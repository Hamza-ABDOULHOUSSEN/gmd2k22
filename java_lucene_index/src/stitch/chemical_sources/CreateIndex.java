package stitch.chemical_sources;

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
    static final File INDEX_DIR = new File("stitch_chemical_sources_index");
    static public String filepath = "../data/STITCH_ATC/chemical.sources.v5.0_reduced.tsv";

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
                String chemical = "";
                String alias = "";
                String source_format = "";
                String source_code = "";

                //skip header
                int line_count = 9;
                for (int i=0; i<line_count; i++) {
                    br.readLine();
                }

                while ((line = br.readLine()) != null) {
                    // new chemical

                    String[] fields = line.split("\t");
                    chemical = fields[0];
                    alias = fields[1];
                    source_format = fields[2];
                    source_code = fields[3];

                    if (eltCount==0) {
                        System.out.println("chemical : " + chemical); ////////////////////////////////////////////
                        System.out.println("alias : " + alias); ////////////////////////////////////////////
                        System.out.println("source_format : " + source_format); ////////////////////////////////////////////
                        System.out.println("source_code : " + source_code); ////////////////////////////////////////////
                    }

                    Document doc = new Document();
                    doc.add(new TextField("chemical", chemical.toLowerCase(), Field.Store.YES));
                    doc.add(new TextField("alias", alias.toLowerCase(), Field.Store.YES));
                    doc.add(new TextField("source_format", source_format, Field.Store.YES));
                    doc.add(new TextField("source_code", source_code, Field.Store.YES));

                    if (writer.getConfig().getOpenMode() == OpenMode.CREATE) {
                        //System.out.println("adding element with id " + id);
                        writer.addDocument(doc);
                    } else {
                        //System.out.println("updating " + file);
                        writer.updateDocument(new Term("path", file.getPath()), doc);
                    }

                    eltCount++;
                    //clean values
                    chemical = "";
                    alias = "";
                    source_format = "";
                    source_code = "";

                }

                br.close();
            } catch (Exception e) {
                System.out.println(e.toString());
            }
        }
        System.out.println(eltCount + " elements have been added to the index " + System.getProperty("user.dir") + "/" + INDEX_DIR);
    }
}