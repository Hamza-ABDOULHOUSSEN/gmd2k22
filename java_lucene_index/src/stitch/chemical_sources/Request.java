package stitch.chemical_sources;

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

public class Request {

    public static void Search(String[] fields, String userQuery) throws IOException, ParseException {
        final String INDEX = "stitch_chemical_sources_index";

        IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(INDEX).toPath()));
        IndexSearcher searcher = new IndexSearcher(reader);
        Analyzer analyzer = new StandardAnalyzer();
        MultiFieldQueryParser parser = new MultiFieldQueryParser(fields, analyzer);
        parser.setAllowLeadingWildcard(true);
        Query query = parser.parse(userQuery);

        //System.out.println("Searching for: " + userQuery);
        TotalHitCountCollector collector = new TotalHitCountCollector();

        // Recherche
        searcher.search(query, collector);
        ScoreDoc[] results = searcher.search(query, Math.max(1, collector.getTotalHits())).scoreDocs;

        // display results
        //System.out.println("Found " + numTotalHits + " hits in " + (end.getTime() - start.getTime()) + " milliseconds");
        for (int i = 0; i < results.length; ++i) {
            int docId = results[i].doc;
            Document doc = searcher.doc(docId);
            String sep = "#-#";
            System.out.println(doc.get("chemical")+sep +doc.get("alias")+sep +doc.get("source_format")+sep +doc.get("source_code"));
        }
    }

    public static void main(String[] args) throws Exception {

        String[] fields = new String[]{"chemical", "alias", "source_format", "source_code"};

        String userQuery = args[0];

        Search(fields, userQuery);

    }
}


