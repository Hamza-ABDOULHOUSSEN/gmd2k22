package hpo;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.MultiFieldQueryParser;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.search.*;
import org.apache.lucene.store.FSDirectory;

import java.io.File;
import java.io.IOException;
import java.util.Date;

public class Request {

    public static void Search(String[] fields, String userQuery) throws IOException, ParseException {
        final String INDEX = "hpo_index";

        IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(INDEX).toPath()));
        IndexSearcher searcher = new IndexSearcher(reader);
        Analyzer analyzer = new StandardAnalyzer();
        Query query = new MultiFieldQueryParser(fields, analyzer).parse(userQuery);

        //System.out.println("Searching for: " + userQuery);
        int hitsPerPage = 10;
        TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage, 10*hitsPerPage);

        // Recherche
        Date start = new Date();
        searcher.search(query, collector);
        Date end = new Date();

        int numTotalHits = collector.getTotalHits();
        ScoreDoc[] results = collector.topDocs().scoreDocs;
        // display results
        //System.out.println("Found " + numTotalHits + " hits in " + (end.getTime() - start.getTime()) + " milliseconds");
        for (int i = 0; i < results.length; ++i) {
            int docId = results[i].doc;
            Document doc = searcher.doc(docId);
            String sep = "#-#";
            System.out.println(doc.get("hpo_id")+sep +doc.get("symptom")+sep +doc.get("synonyms")+sep +doc.get("is_a"));
        }
    }

    public static void main(String[] args) throws Exception {

        String[] fields = new String[]{"hpo_id", "symptom", "synonyms", "is_a"};

        String userQuery = args[0];

        Search(fields, userQuery);

    }
}


