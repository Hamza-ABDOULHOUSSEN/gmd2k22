import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.MultiFieldQueryParser;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.store.FSDirectory;

import java.io.File;
import java.io.IOException;
import java.util.Date;

public class Request {

    public static void Search(String[] fields, String userQuery) throws IOException, ParseException {
        String index = "drug_bank_index";

        IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(index).toPath()));
        IndexSearcher searcher = new IndexSearcher(reader);
        Analyzer analyzer = new StandardAnalyzer();
        Query query = new MultiFieldQueryParser(fields, analyzer).parse(userQuery);

        System.out.println("Searching for: " + userQuery);
        int hitsPerPage = 10;
        TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage, 10*hitsPerPage);

        // Recherche
        Date start = new Date();
        searcher.search(query, collector);
        Date end = new Date();

        int numTotalHits = collector.getTotalHits();
        ScoreDoc[] results = collector.topDocs().scoreDocs;
        // display results
        System.out.println("Found " + numTotalHits + " hits in " + (end.getTime() - start.getTime()) + " milliseconds");
        for (int i = 0; i < results.length; ++i) {
            int docId = results[i].doc;
            Document doc = searcher.doc(docId);
            System.out.println((i + 1) + ". " + doc.get("id") + ", generic name = " + doc.get("Generic_Name"));
        }
    }

    public static void main(String[] args) throws Exception {

        String[] fields;
        String userQuery;

        // Question 4
        System.out.println("\n=========================== Question 4 ===========================\n");

        //fields = new String[]{"Generic_Name", "Synonyms", "Brand_Names"};
        fields = new String[]{"Generic_Name", "Synonyms", "Brand_Names", "Indication"};
        userQuery = "aspirin";

        Search(fields, userQuery);

        System.out.println("\n=========================== Question 5 ===========================\n");

        //fields = new String[]{"description", "indication"};
        fields = new String[]{"Generic_Name", "Synonyms", "Brand_Names", "Indication"};
        userQuery = "diabetes";

        Search(fields, userQuery);

        System.out.println("\n=========================== Question 6 ===========================\n");

        //fields = new String[]{"drugInteractions"};
        fields = new String[]{"Generic_Name", "Synonyms", "Brand_Names", "Indication"};
        userQuery = "mercaptopurine";

        Search(fields, userQuery);

    }
}


