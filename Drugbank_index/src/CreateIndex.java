import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StoredField;
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
    static public String filepath = "../DRUGBANK/drugbank.xml";

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
                String genericName = "";
                String synonyms = "";
                String brandNames = "";
                String description = "";
                String indication = "";
                String pharmacology = "";
                String drugInteractions = "";
                while ((line = br.readLine()) != null) {
                    // new drug
                    if (line.startsWith("#BEGIN_DRUGCARD ")) {
                        String[] fields = line.split(" ");
                        id = fields[1];
                    }
                    if (line.equals("# Generic_Name:")) {
                        if ((line = br.readLine()) != null)
                            genericName = line;
                    }
                    if (line.equals("# Synonyms:")) {
                        while ((line = br.readLine()) != null) {
                            if (line.equals("")) {
                                break;
                            } else {
                                synonyms += line + " ";
                            }
                        }
                    }
                    if (line.equals("# Brand_Names:")) {
                        while ((line = br.readLine()) != null) {
                            if (line.equals("")) {
                                break;
                            } else {
                                brandNames += line + " ";
                            }
                        }
                    }
                    if (line.equals("# Description:")) {
                        if ((line = br.readLine()) != null)
                            description = line;
                    }
                    if (line.equals("# Indication:")) {
                        if ((line = br.readLine()) != null)
                            indication = line;
                    }
                    if (line.equals("# Pharmacology:")) {
                        if ((line = br.readLine()) != null)
                            pharmacology = line;
                    }
                    if (line.equals("# Drug_Interactions:")) {
                        while ((line = br.readLine()) != null) {
                            if (line.equals("")) {
                                break;
                            } else {
                                drugInteractions += line + " ";
                            }
                        }
                    }
                    if (line.startsWith("#END_DRUGCARD ")) {
                        //write the index
                        // make a new, empty document
                        Document doc = new Document();
                        doc.add(new StoredField("id", id)); // stored not indexed
                        doc.add(new TextField("Generic_Name", genericName.toLowerCase(), Field.Store.YES)); // indexed and stored
                        doc.add(new TextField("Synonyms", synonyms, Field.Store.NO)); // indexed
                        doc.add(new TextField("Brand_Names", brandNames, Field.Store.NO)); // indexed
                        doc.add(new TextField("Description", description, Field.Store.NO)); // indexed
                        doc.add(new TextField("Indication", indication, Field.Store.NO)); // indexed
                        doc.add(new TextField("Pharmacology", pharmacology, Field.Store.NO)); // indexed
                        doc.add(new TextField("Drug_Interactions", drugInteractions, Field.Store.NO)); // indexed

                        if (writer.getConfig().getOpenMode() == OpenMode.CREATE) {
                            System.out.println("adding element with id " + id);
                            writer.addDocument(doc);
                        } else {
                            System.out.println("updating " + file);
                            writer.updateDocument(new Term("path", file.getPath()), doc);
                        }

                        eltCount++;
                        //clean values
                        id = "";
                        genericName = "";
                        synonyms = "";
                        brandNames = "";
                        description = "";
                        indication = "";
                        pharmacology = "";
                        drugInteractions = "";
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