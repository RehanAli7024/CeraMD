import React, { useState, useEffect, useRef } from "react";
import { createClient, LiveTranscriptionEvents } from "@deepgram/sdk";
import { jsPDF } from "jspdf";
import { Mic, MicOff, FileText, Stethoscope, ClipboardList, Trash2, FileDown, Loader2 } from "lucide-react";

import "./AudioRecorder.css";

const AudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcripts, setTranscripts] = useState([]);
  const [processedTranscript, setProcessedTranscript] = useState(null);
  const API_KEY =import.meta.env.VITE_API_KEY;
  const deepgramRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const [soapNote, setSOAPNote] = useState(null);
  const [differentialDiagnosis, setDifferentialDiagnosis] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [activeView, setActiveView] = useState("transcript");

  useEffect(() => {
    const client = createClient(API_KEY);

    const setupDeepgram = () => {
      deepgramRef.current = client.listen.live({
        language: "en-US",
        punctuate: true,
        interim_results: false,
        diarize: true,
        model: "nova-2-general",
      });

      deepgramRef.current.addListener(LiveTranscriptionEvents.Open, () => {
        console.log("Deepgram connection established");
      });

      deepgramRef.current.addListener(
        LiveTranscriptionEvents.Transcript,
        (data) => {
          if (
            data.is_final &&
            data.channel.alternatives[0].transcript.trim() !== ""
          ) {
            const newTranscript = {
              speaker: data.channel.alternatives[0].speaker || "Stranger",
              text: data.channel.alternatives[0].transcript,
              timestamp: new Date().toISOString(),
            };
            setTranscripts((prev) => [...prev, newTranscript]);
          }
        }
      );
    };

    const startRecording = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        mediaRecorderRef.current = new MediaRecorder(stream);

        mediaRecorderRef.current.addEventListener("dataavailable", (event) => {
          if (
            event.data.size > 0 &&
            deepgramRef.current.getReadyState() === 1
          ) {
            deepgramRef.current.send(event.data);
          }
        });

        mediaRecorderRef.current.start(1000);
        setupDeepgram();
      } catch (error) {
        console.error("Error accessing microphone:", error);
      }
    };

    const stopRecording = () => {
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
      }
      if (deepgramRef.current) {
        deepgramRef.current.finish();
      }
    };

    if (isRecording) {
      startRecording();
    } else {
      stopRecording();
    }

    return () => {
      if (deepgramRef.current) {
        deepgramRef.current.finish();
      }
    };
  }, [isRecording, API_KEY]);

  const toggleRecording = () => {
    setIsRecording(!isRecording);
  };
  
  const clearAll = () => {
    setTranscripts([]);
    setProcessedTranscript(null);
    setSOAPNote(null);
    setDifferentialDiagnosis(null);
    setActiveView("transcript");
  };

  const processTranscript = async () => {
    const data = {
      transcript: transcripts,
    };
    setIsLoading(true);

    try {
      const response = await fetch("https://ceramd-1.onrender.com/process-transcript", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const result = await response.json();
        setProcessedTranscript(result);
        setActiveView("processed");
      } else {
        console.error("Failed to process transcript");
      }
    } catch (error) {
      console.error("Error processing transcript:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const generateSOAPNote = async () => {
    if (!processedTranscript) return;
    setIsLoading(true);
    try {
      const response = await fetch("https://ceramd-1.onrender.com/generate-soap", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(processedTranscript),
      });

      if (response.ok) {
        const result = await response.json();
        setSOAPNote(result.soap_note);
        setActiveView("soap");
        console.log("SOAP note generated successfully");
      } else {
        console.error("Failed to generate SOAP note");
      }
    } catch (error) {
      console.error("Error generating SOAP note:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const generateDifferentialDiagnosis = async () => {
    if (!soapNote) return;
    setIsLoading(true);
    try {
      const response = await fetch(
        "https://ceramd-1.onrender.com/generate-differential-diagnosis",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ soap_note: soapNote }),
        }
      );

      if (response.ok) {
        const result = await response.json();
        setDifferentialDiagnosis(result.differential_diagnosis);
        setActiveView("diagnosis");
        console.log("Differential diagnosis generated successfully");
      } else {
        console.error("Failed to generate differential diagnosis");
      }
    } catch (error) {
      console.error("Error generating differential diagnosis:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const saveAsPDF = () => {
    if (!processedTranscript && !soapNote && !differentialDiagnosis) return;

    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.width;
    const margin = 10;
    const maxLineWidth = pageWidth - 2 * margin;

    doc.setFontSize(14);
    let title = "Transcript";
    if (soapNote && activeView === "soap") title = "SOAP Note";
    if (differentialDiagnosis && activeView === "diagnosis") title = "Differential Diagnosis";
    doc.text(title, margin, margin);

    doc.setFontSize(10);
    let y = margin + 10;

    if (differentialDiagnosis && activeView === "diagnosis") {
      const lines = doc.splitTextToSize(differentialDiagnosis, maxLineWidth);
      doc.text(lines, margin, y);
      y += lines.length * 5;
    } else if (soapNote && activeView === "soap") {
      const lines = doc.splitTextToSize(soapNote, maxLineWidth);
      doc.text(lines, margin, y);
      y += lines.length * 5;
    } else {
      processedTranscript.transcript.forEach((entry) => {
        const speakerText = `${entry.speaker}: `;
        const contentText = entry.text;
       

        doc.setFont(undefined, "bold");
        doc.text(speakerText, margin, y);

        const speakerWidth = doc.getTextWidth(speakerText);
        doc.setFont(undefined, "normal");

        const contentLines = doc.splitTextToSize(
          contentText,
          maxLineWidth - speakerWidth
        );
        doc.text(contentLines, margin + speakerWidth, y);

        y += contentLines.length * 5;

        doc.setFontSize(8);
       
        doc.setFontSize(10);

        y += 8;

        if (y > doc.internal.pageSize.height - margin) {
          doc.addPage();
          y = margin;
        }
      });
    }
    const patientName = processedTranscript?.patient_name || "Unknown";
    const fileName = `${patientName}_${title.replace(" ", "_")}.pdf`;
    doc.save(fileName);
  };
  
  const LoadingSpinner = () => (
    <div className="loading-spinner">
      <div className="spinner"></div>
    </div>
  );

  const renderContent = () => {
    if (isLoading) {
      return <LoadingSpinner />;
    }
    
    switch (activeView) {
      case "diagnosis":
        return differentialDiagnosis ? (
          <div className="differential-diagnosis">
            <h3>Differential Diagnosis</h3>
            <pre>{differentialDiagnosis}</pre>
          </div>
        ) : null;
      case "soap":
        return soapNote ? (
          <div className="soap-note">
            <h3>SOAP Note</h3>
            <pre>{soapNote}</pre>
          </div>
        ) : null;
      case "processed":
        return processedTranscript ? (
          <div>
            <h3>Processed Transcript</h3>
            {processedTranscript.transcript.map((entry, index) => (
              <div key={index} className="transcript-entry">
                <span className="speaker">{entry.speaker}:</span> {entry.text}
                
              </div>
            ))}
          </div>
        ) : null;
      case "transcript":
      default:
        return (
          <div>
            <h3>Live Transcript</h3>
            {transcripts.length > 0 ? (
              transcripts.map((entry, index) => (
                <div key={index} className="transcript-entry">
                  <span className="speaker">{entry.speaker}:</span> {entry.text}
                 
                </div>
              ))
            ) : (
              <div className="empty-state">
                <p>No transcript available yet. Click "Start Recording" to begin.</p>
              </div>
            )}
          </div>
        );
    }
  };

  return (
    <div className="audio-recorder">
      <div className="header">
        <h2>
          <span className="logo-icon">
            <Stethoscope size={28} />
          </span>
          CeraMD
        </h2>
        <p className="tagline">AI-Powered Medical Transcription & Analysis</p>
      </div>
      
      <div className="tabs">
        <button 
          className={`tab ${activeView === 'transcript' ? 'active' : ''}`}
          onClick={() => setActiveView('transcript')}
          disabled={transcripts.length === 0}
        >
          Live Transcript
        </button>
        <button 
          className={`tab ${activeView === 'processed' ? 'active' : ''}`}
          onClick={() => setActiveView('processed')}
          disabled={!processedTranscript}
        >
          Processed
        </button>
        <button 
          className={`tab ${activeView === 'soap' ? 'active' : ''}`}
          onClick={() => setActiveView('soap')}
          disabled={!soapNote}
        >
          SOAP Note
        </button>
        <button 
          className={`tab ${activeView === 'diagnosis' ? 'active' : ''}`}
          onClick={() => setActiveView('diagnosis')}
          disabled={!differentialDiagnosis}
        >
          Diagnosis
        </button>
      </div>
      
      <div className="button-group">
        <button 
          className={`button ${isRecording ? 'button-stop' : 'button-record'}`} 
          onClick={toggleRecording}
        >
          {isRecording ? (
            <>
              <MicOff size={18} /> Stop Recording
            </>
          ) : (
            <>
              <Mic size={18} /> Start Recording
            </>
          )}
        </button>
        <button
          className="button button-process"
          onClick={processTranscript}
          disabled={transcripts.length === 0}
        >
          <FileText size={18} /> Process Transcript
        </button>
        <button
          className="button button-generate-soap"
          onClick={generateSOAPNote}
          disabled={!processedTranscript}
        >
          <ClipboardList size={18} /> Generate SOAP Note
        </button>
        <button
          className="button button-generate-diagnosis"
          onClick={generateDifferentialDiagnosis}
          disabled={!soapNote}
        >
          <Stethoscope size={18} /> Generate Diagnosis
        </button>
        <button
          className="button button-clear"
          onClick={clearAll}
          disabled={transcripts.length === 0}
        >
          <Trash2 size={18} /> Clear All
        </button>
        <button
          className="button button-save-pdf"
          onClick={saveAsPDF}
          disabled={!processedTranscript && !soapNote && !differentialDiagnosis}
        >
          <FileDown size={18} /> Save as PDF
        </button>
      </div>
      
      <div className="content-container">
        {renderContent()}
      </div>
      
      {processedTranscript && (
        <div className="patient-info">
          <div className="info-item">
            <span className="info-label">Patient:</span>
            <span className="info-value">{processedTranscript.patient_name || "Unknown"}</span>
          </div>
          {processedTranscript.patient_age && (
            <div className="info-item">
              <span className="info-label">Age:</span>
              <span className="info-value">{processedTranscript.patient_age}</span>
            </div>
          )}
          {processedTranscript.patient_gender && (
            <div className="info-item">
              <span className="info-label">Gender:</span>
              <span className="info-value">{processedTranscript.patient_gender}</span>
            </div>
          )}
          {processedTranscript.doctor_name && (
            <div className="info-item">
              <span className="info-label">Doctor:</span>
              <span className="info-value">{processedTranscript.doctor_name}</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AudioRecorder;