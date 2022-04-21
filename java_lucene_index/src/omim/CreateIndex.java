package omim;

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
import java.util.Locale;

public class CreateIndex {
    static final File INDEX_DIR = new File("omim_index");
    static public String filepath = "../data/OMIM/omim.txt";

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
                String omim_id = "";
                String field0 = "";
                String field1 = "";
                String symptoms = "";

                //skip header
                int line_count = 1;
                for (int i=0; i<line_count; i++) {
                    br.readLine();
                }

                while ((line = br.readLine()) != null) {

                    // new record
                    if (line.startsWith("*FIELD* NO")) {
                        omim_id = br.readLine();

                        if (eltCount==4) {
                            System.out.println("id : " + omim_id);
                        }
                    }

                    if (line.startsWith("*FIELD* CS")) {
                        line = br.readLine();
                        String[] fields;
                        while (!line.startsWith("*")) {
                            if (line.contains(":")) {
                                fields = line.split(":");
                                field0 = fields[0];
                                line = br.readLine();
                            }
                            else if (line.contains("[")) {
                                fields = line.split("\\[");
                                fields = fields[1].split("]");
                                field1 = fields[0];
                                line = br.readLine();
                            }
                            else if (line.length() != 0) {
                                if (line.contains(";")) {
                                    fields = line.split(";");
                                    symptoms = fields[0].trim();
                                    symptoms = symptoms.replaceAll("\t", "");
                                    line = br.readLine();
                                }
                                else {
                                    symptoms = line.trim();
                                    line = br.readLine();
                                    while (line.length()!=0 && !line.contains(":") && !line.contains("[")) {
                                        String rest;
                                        if (line.contains(";")) {
                                            fields = line.split(";");
                                            rest = fields[0].trim();
                                            rest = rest.replaceAll("\t", "");
                                        }
                                        else {
                                            //fields = line.split("\t");
                                            rest = line.trim();
                                            rest = rest.replaceAll("\t", "");
                                        }

                                        // write in symptoms
                                        if (symptoms.equals("")) {
                                            symptoms = rest;
                                        }
                                        else {
                                            symptoms = symptoms + " " + rest;
                                        }

                                        line = br.readLine();
                                    }
                                }

                                if (eltCount==4) {
                                    System.out.println("field0 : " + field0);
                                    System.out.println("field1 : " + field1);
                                    System.out.println("symptoms : " + symptoms);
                                }

                                //write the index
                                // make a new, empty document
                                Document doc = new Document();
                                doc.add(new TextField("omim_id", omim_id, Field.Store.YES));
                                doc.add(new TextField("field0", field0.toLowerCase(), Field.Store.YES));
                                doc.add(new TextField("field1", field1.toLowerCase(), Field.Store.YES));
                                doc.add(new TextField("symptoms", symptoms.toLowerCase(), Field.Store.YES));

                                if (writer.getConfig().getOpenMode() == OpenMode.CREATE) {
                                    //System.out.println("adding element with id " + id);
                                    writer.addDocument(doc);
                                } else {
                                    //System.out.println("updating " + file);
                                    writer.updateDocument(new Term("path", file.getPath()), doc);
                                }
                            }
                            else {
                                line = br.readLine();
                            }
                        }

                        eltCount++;

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