package stitch.br08303;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.index.Term;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import java.io.*;
import java.util.Date;

public class CreateIndex {
    static final File INDEX_DIR = new File("stitch_br08303_index");
    static public String filepath = "../data/STITCH_ATC/br08303.keg";

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
                String atc_code = "";
                String drug_name = "";

                //skip header
                int line_count = 9;
                for (int i=0; i<line_count; i++) {
                    br.readLine();
                }

                while ((line = br.readLine()) != null && !(line.startsWith("!"))) {

                    if (!line.startsWith("#")) {

                        // new drug
                        line = line.substring(1);

                        // remove space from the beginning and end
                        line = line.trim();

                        // split in two to get atc_code and drug name
                        String[] fields = line.split(" ", 2);
                        atc_code = fields[0];
                        drug_name = fields[1];

                        if (eltCount < 15) {
                            System.out.println("atc_code : " + atc_code); ////////////////////////////////////////////
                            System.out.println("drug_name : " + drug_name); ////////////////////////////////////////////
                        }

                        //write the index
                        Document doc = new Document();
                        doc.add(new TextField("atc_code", atc_code, Field.Store.YES));
                        doc.add(new TextField("drug_name", drug_name, Field.Store.YES));

                        if (writer.getConfig().getOpenMode() == OpenMode.CREATE) {
                            //System.out.println("adding element with id " + id);
                            writer.addDocument(doc);
                        } else {
                            //System.out.println("updating " + file);
                            writer.updateDocument(new Term("path", file.getPath()), doc);
                        }


                        eltCount++;
                        //clean values
                        atc_code = "";
                        drug_name = "";
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