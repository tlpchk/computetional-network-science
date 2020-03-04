package com.telepchuk.cns.gephi;

import org.gephi.algorithms.shortestpath.DijkstraShortestPathAlgorithm;
import org.gephi.graph.api.GraphController;
import org.gephi.graph.api.GraphModel;
import org.gephi.graph.api.Node;
import org.gephi.io.importer.api.Container;
import org.gephi.io.importer.api.ImportController;
import org.gephi.io.processor.plugin.DefaultProcessor;
import org.gephi.project.api.ProjectController;
import org.gephi.project.api.Workspace;
import org.gephi.statistics.plugin.*;
import org.openide.util.Lookup;

import java.io.File;
import java.io.FileNotFoundException;
import java.net.URISyntaxException;

public class NetworkAnalyzer {
    GraphModel graphModel;
    long start;

    public NetworkAnalyzer(String resource) {
        ProjectController pc = Lookup.getDefault().lookup(ProjectController.class);
        pc.newProject();
        Workspace workspace = pc.getCurrentWorkspace();

        ImportController ic = Lookup.getDefault().lookup(ImportController.class);
        Container container = null;
        try {
            var uri = getClass().getResource(resource).toURI();
            File file = new File(uri);
            container = ic.importFile(file);
            container.getLoader().setAllowAutoNode(false);
        } catch (URISyntaxException | FileNotFoundException e) {
            e.printStackTrace();
        }

        ic.process(container, new DefaultProcessor(), workspace);

        this.graphModel = Lookup.getDefault().lookup(GraphController.class).getGraphModel();
    }

    // degree
    public void degree() {
        var degree = new Degree();
        degree.execute(graphModel);
    }

    // betweeness, cloeseness
    public void distance() {
        var distance = new GraphDistance();
        distance.execute(graphModel);
    }

    // clustering cofficient
    public void clusteringCofficient() {
        var clustering = new ClusteringCoefficient();
        clustering.execute(graphModel);
    }

    // page rank
    public void pageRank() {
        var pageRank = new PageRank();
        pageRank.execute(graphModel);
    }

    // shortest paths
    public void shortestPaths() {
        var nodes = graphModel.getGraph().getNodes().toArray();
        for (Node n : nodes) {
            var dijkstra = new DijkstraShortestPathAlgorithm(graphModel.getGraph(), n);
            dijkstra.compute();
        }
    }

    // diameter
    public void diameter() {
        //TODO
    }

    //connected components
    public void connectedComponents() {
        var cc = new ConnectedComponents();
        cc.execute(graphModel);
    }

    //density
    public void density() {
        var graphDensity = new GraphDensity();
        graphDensity.execute(graphModel);
    }

    public void tic() {
        start = System.currentTimeMillis();
    }

    public void tac(String label) {
        long end = System.currentTimeMillis();
        float sec = (end - start) / 1000F;
        System.out.printf("%s : %f seconds\n", label, sec);
    }

    public void analyze() {
        tic();
        degree();
        tac("degree");

        tic();
        distance();
        tac("betweenness, closeness");

        tic();
        clusteringCofficient();
        tac("clusteringCofficient");

        tic();
        pageRank();
        tac("pageRank");

        tic();
        shortestPaths();
        tac("shortestPaths");

        tic();
        connectedComponents();
        tac("connectedComponents");

        tic();
        density();
        tac("density");
    }

}
