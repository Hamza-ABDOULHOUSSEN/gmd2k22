package drugbank;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.index.Term;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.index.IndexWriterConfig;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.io.BufferedReader;
import java.util.Date;

public class CreateIndex {
    static final File INDEX_DIR = new File("drug_bank_index");
    static public String filepath = "../data/DRUGBANK/drugbank.xml";

    /**
     * Index all lines of a text file
     */
    public static void main(String[] args) {

        if (INDEX_DIR.exists()) {
            System.out.println("Cannot save index to '" + INDEX_DIR + "' directory, please delete it first");
            System.exit(1);
        }

        if (args.length == 1) {
            filepath = args[0];
        }

        final File file = new File(filepath);
        if (!file.exists() || !file.canRead()) {
            System.out.println("File '" + file.getAbsolutePath() + "' does not exist or is not readable, please check the path");
            System.exit(1);
        }

        Date start = new Date();
        try {
            Directory directory = FSDirectory.open(INDEX_DIR.toPath());
            Analyzer analyzer = new StandardAnalyzer();
            IndexWriterConfig config = new IndexWriterConfig(analyzer);

            IndexWriter writer = new IndexWriter(directory, config);

            System.out.println("Indexing to directory '" + INDEX_DIR + "'...");
            indexDoc(writer, file);
            writer.close();

            Date end = new Date();
            System.out.println(end.getTime() - start.getTime() + " total milliseconds");

        } catch (IOException e) {
            System.out.println(" caught a " + e.getClass() +
                    "\n with message: " + e.getMessage());
        }
    }

    private static void indexDoc(IndexWriter writer, File file) throws IOException {
        int eltCount = 0;

        if (file.canRead() && !file.isDirectory()) {
            // each line of the file is a new document
            try {
                InputStream ips = new FileInputStream(file);
                InputStreamReader ipsr = new InputStreamReader(ips);
                BufferedReader br = new BufferedReader(ipsr);
                String line;
                //initialization
                String id = "";
                String name = "";
                String synonyms = "";
                String description = "";
                String indication = "";
                String toxicity = "";
                String atccode = "";

                while ((line = br.readLine()) != null) {
                    // new drug
                    if (line.startsWith("  <drugbank-id primary=\"true\">")) {
                        String[] fields = line.split("  <drugbank-id primary=\"true\">");
                        fields = fields[1].split("</drugbank-id>");
                        id = fields[0];
                        if (eltCount==0) {
                            System.out.println("id : " + id); ////////////////////////////////////////////
                        }
                    }

                    if (line.startsWith("  <name>")) {
                        String[] fields = line.split("  <name>");
                        fields = fields[1].split("</name>");
                        name = fields[0];
                        if (eltCount==0) {
                            System.out.println("name : " + name); ////////////////////////////////////////////
                        }
                    }

                    if (line.startsWith("  <description>")) {
                        String[] fields = line.split("  <description>");
                        fields = fields[1].split("</description>");
                        description = fields[0];
                        if (eltCount==0) {
                            System.out.println("description : " + description); ////////////////////////////////////////////
                        }
                    }

                    if (line.startsWith("  <indication>")) {
                        String[] fields = line.split("  <indication>");
                        fields = fields[1].split("</indication>");
                        indication = fields[0];
                        if (eltCount==0) {
                            System.out.println("indication : " + indication); ////////////////////////////////////////////
                        }
                    }

                    if (line.startsWith("  <toxicity>")) {
                        String[] fields = line.split("  <toxicity>");
                        fields = fields[1].split("</toxicity>");
                        toxicity = fields[0];
                        if (eltCount==0) {
                            System.out.println("toxicity : " + toxicity); ////////////////////////////////////////////
                        }
                    }

                    if (line.startsWith("  <synonyms>")) {
                        while ((line = br.readLine()) != null) {
                            if (line.startsWith("  </synonyms>")) {
                                break;
                            } else {
                                String[] fields = line.split(">");
                                fields = fields[1].split("<");
                                synonyms = synonyms + "," + fields[0];
                            }
                        }
                        synonyms = synonyms.substring(1);
                        if (eltCount==0) {
                            System.out.println("synonyms : " + synonyms); ////////////////////////////////////////////
                        }
                    }

                    if (line.startsWith("    <atc-code")) {
                        String[] fields = line.split("\"");
                        atccode = fields[1];
                        if (eltCount==0) {
                            System.out.println("atc_code : " + atccode); ////////////////////////////////////////////
                        }
                    }

                    if (line.startsWith("</drug>")) {
                        //write the index
                        // make a new, empty document
                        Document doc = new Document();
                        doc.add(new TextField("id", id, Field.Store.YES));
                        doc.add(new TextField("name", name.toLowerCase(), Field.Store.YES));
                        doc.add(new TextField("synonyms", synonyms, Field.Store.YES));
                        doc.add(new TextField("description", description, Field.Store.YES));
                        doc.add(new TextField("indication", indication, Field.Store.YES));
                        doc.add(new TextField("toxicity", toxicity, Field.Store.YES));
                        doc.add(new TextField("atc_code", atccode, Field.Store.YES));

                        if (writer.getConfig().getOpenMode() == OpenMode.CREATE) {
                            //System.out.println("adding element with id " + id);
                            writer.addDocument(doc);
                        } else {
                            //System.out.println("updating " + file);
                            writer.updateDocument(new Term("path", file.getPath()), doc);
                        }

                        eltCount++;
                        //clean values
                        id = "";
                        name = "";
                        synonyms = "";
                        description = "";
                        indication = "";
                        toxicity = "";
                        atccode = "";
                    }
                }

                br.close();
            } catch (Exception e) {
                System.out.println(e.toString());
            }
        }
        System.out.println(eltCount + " elements have been added to the index " + System.getProperty("user.dir") + "/" + INDEX_DIR);
    }
}