package hpo;

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
    static final File INDEX_DIR = new File("hpo_index");
    static public String filepath = "../data/HPO/hpo.obo";

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
                String hpo_id = "";
                String symptom = "";
                String synonyms = "";
                String is_a = "";

                //skip header
                int line_count = 29;
                for (int i=0; i<line_count; i++) {
                    br.readLine();
                }

                while ((line = br.readLine()) != null) {

                    // new symptom
                    if (line.startsWith("id:")) {
                        String[] fields = line.split("id: ");
                        hpo_id = fields[1];

                    }

                    if (line.startsWith("name: ")) {
                        String[] fields = line.split("name: ");
                        symptom = fields[1];
                    }

                    if (line.startsWith("synonym: ")) {
                        String[] fields = line.split("\"");
                        String synonym = fields[1];
                        synonyms = "," + synonym;
                    }

                    if (line.startsWith("is_a: ")) {
                        String[] fields = line.split(" ");
                        String one_is_a = fields[1];
                        is_a = "," + one_is_a;
                    }

                    if (line.length() == 0) {

                        // corrections
                        hpo_id = hpo_id.replaceAll(":", "_"); //issues for lucene queries with :
                        if (synonyms.length() != 0)
                            synonyms = synonyms.substring(1);
                        if (is_a.length() != 0) {
                            is_a = is_a.substring(1);
                            is_a = is_a.replaceAll(":", "_");
                        }

                        // print one to check
                        if (eltCount==1) {
                            System.out.println("hpo_id : " + hpo_id); ////////////////////////////////////////////
                            System.out.println("symptom : " + symptom); ////////////////////////////////////////////
                            System.out.println("synonyms : " + synonyms); ////////////////////////////////////////////
                            System.out.println("is_a : " + is_a); ////////////////////////////////////////////
                        }

                        //write the index
                        // make a new, empty document
                        Document doc = new Document();
                        doc.add(new TextField("hpo_id", hpo_id, Field.Store.YES));
                        doc.add(new TextField("symptom", symptom.toLowerCase(), Field.Store.YES));
                        doc.add(new TextField("synonyms", synonyms.toLowerCase(), Field.Store.YES));
                        doc.add(new TextField("is_a", is_a.toLowerCase(), Field.Store.YES));

                        if (writer.getConfig().getOpenMode() == OpenMode.CREATE) {
                            //System.out.println("adding element with id " + id);
                            writer.addDocument(doc);
                        } else {
                            //System.out.println("updating " + file);
                            writer.updateDocument(new Term("path", file.getPath()), doc);
                        }

                        eltCount++;
                        //clean values
                        hpo_id = "";
                        symptom = "";
                        synonyms = "";
                        is_a = "";
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