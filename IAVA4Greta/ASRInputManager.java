/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package greta.FlipperDemo.input;

/**
 *
 * @author Jieyeon Woo
 */

import ch.qos.logback.classic.util.ContextInitializer;
import greta.FlipperDemo.dm.managers.FMLManager;
import greta.FlipperDemo.main.FlipperLauncherMain;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

public class ASRInputManager {
    
   
    
   private SpeechInputReceiver  inputReceiver;
   private FlipperLauncherMain singletoneInstance = null;
   
   private String host = null;
   private String port = null;
   private String gretaASRTopic = null;
   private String gretaInputTopic = null;
   private String msg;
   
   
   public boolean init()
   {   System.out.println("ASR input manager initialized");
       singletoneInstance = FlipperLauncherMain.getInstance();
       if(singletoneInstance != null){
           System.out.println("jai gayatri mata: asrinput got main singleton instance : "
                   + singletoneInstance.getGretaASRTopic());
       }
       
       host = singletoneInstance.getHost();
       port = singletoneInstance.getPort();
       gretaASRTopic = singletoneInstance.getGretaASRTopic();
       inputReceiver = new SpeechInputReceiver(host, port, gretaASRTopic);
       
       
       
       return true;
   }
   public void initSpeechInputReceiver(String host, String port, String topic){
       inputReceiver = new SpeechInputReceiver(host, port, topic);
   }
   
    public boolean hasMessage(){
        return inputReceiver.hasMessage();
    }
    
     public String getMessage(){
         this.msg = inputReceiver.getMessage();
         return msg;
     }
     
     // Check if the received message is an Automatic Thought via ATcls
     public String checkMessageIsAT() throws IOException {
        String isAT="";;
        try {
            Process process = new ProcessBuilder("python", System.getProperty("user.dir")+"\\Scripts\\ATcls\\ATclassifyFR.py").redirectErrorStream(true).start();
            
            BufferedWriter pythonInput = new BufferedWriter(new OutputStreamWriter(process.getOutputStream() )); //,"ISO-8859-15"));
            BufferedReader pythonOutput = new BufferedReader(new InputStreamReader(process.getInputStream()));
            
            Thread thread = new Thread(() -> {
                while(process.isAlive()){
                    try{
                        pythonInput.write(this.msg);
                        pythonInput.newLine();
                        pythonInput.flush();
                    } catch (IOException ex) {
                        System.out.println(ex.getLocalizedMessage());
                        process.destroy();
                        System.out.println("Python program terminated");
                        Logger.getLogger(ASRInputManager.class.getName()).log(Level.SEVERE, null, ex);
                    }
                }
            }
            );
            thread.start();
            String output=null;
            StringBuilder sb = new StringBuilder();
            while(process.isAlive() && (output=pythonOutput.readLine())!=null){
                System.out.println("output: "+output);
                sb.append(output);
            }
            isAT = sb.toString();
            pythonOutput.close();
            pythonInput.close();
     
        } catch (IOException ex) {
            Logger.getLogger(FMLManager.class.getName()).log(Level.SEVERE, null, ex);
        }
        System.out.println("Checked ATcls: " + this.msg + " " + isAT + "\n");
        
        return isAT;
    }
     
}
