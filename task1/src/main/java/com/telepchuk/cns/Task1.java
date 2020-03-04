package com.telepchuk.cns;


import com.telepchuk.cns.gephi.NetworkAnalyzer;

public class Task1 {
    public static void main(String[] args) {
        var analyzer = new NetworkAnalyzer("/hypertext-face-contacts/graph.gexf");
        analyzer.analyze();

        System.out.println("-------");

        analyzer = new NetworkAnalyzer("/chicago/graph.gexf");
        analyzer.analyze();


        System.out.println("-------");

        analyzer = new NetworkAnalyzer("/astroph/graph.gexf");
        analyzer.analyze();
    }

}
