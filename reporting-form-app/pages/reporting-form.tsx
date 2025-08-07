import { useEffect, useState } from "react";
import Form from "@rjsf/core";
import validator from "@rjsf/validator-ajv8";
import { reportingFormSchema } from "../schemas/reportingFormSchema";
import Link from "next/link";
import FileUploadWidget from "./filesUploadWidget";
import MultiSelectWidget from './multiSelectWidgets'; // Make sure this import path is correct
import '../src/app/globals.css';

const FORM_KEY = "reportingFormData";

export default function ReportingFormPage() {
  const [formData, setFormData] = useState<any>(null);
  const [marker, setMarker] = useState<{ x: number; y: number } | null>(null);
  const [imageSize, setImageSize] = useState<{ width: number; height: number } | null>(null);

  // Load from localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      try {
        const saved = localStorage.getItem(FORM_KEY);
        if (saved) {
          const parsed = JSON.parse(saved);
          setFormData(parsed);
          const storedX = parsed?.incidents?.injured_diagram?.marker_position?.x;
          const storedY = parsed?.incidents?.injured_diagram?.marker_position?.y;
          if (storedX !== undefined && storedY !== undefined) {
            console.log("Found stored coordinates:", storedX, storedY);
          }
        } else {
          setFormData({});
        }
      } catch (err) {
        console.error("Failed to parse saved form data:", err);
        setFormData({});
      }
    }
  }, []);

  const handleChange = ({ formData }: any) => {
    setFormData(formData);
    localStorage.setItem(FORM_KEY, JSON.stringify(formData));
    
    const markerX = formData?.incidents?.injured_diagram?.marker_position?.x;
    const markerY = formData?.incidents?.injured_diagram?.marker_position?.y;
    
    if (markerX !== undefined && markerY !== undefined && imageSize) {
      const normalizedX = markerX / imageSize.width;
      const normalizedY = markerY / imageSize.height;
      setMarker({ x: normalizedX, y: normalizedY });
    }
  };

  const handleSubmit = ({ formData }: any) => {
    console.log("Submitted!", formData);
    alert("Form submitted");
  };

  const handleReset = () => {
    setFormData({});
    setMarker(null);
    localStorage.removeItem(FORM_KEY);
  };

  const handleImageClick = (e: React.MouseEvent<HTMLImageElement>) => {
    const img = e.currentTarget;
    const rect = img.getBoundingClientRect();
  
    const pixelX = e.clientX - rect.left;
    const pixelY = e.clientY - rect.top;
    const normalizedX = pixelX / rect.width;
    const normalizedY = pixelY / rect.height;
  
    console.log("Pixel coordinates - x:", Math.round(pixelX), "y:", Math.round(pixelY));
    console.log("Normalized coordinates - x:", normalizedX, "y:", normalizedY);
  
    setMarker({ x: normalizedX, y: normalizedY });
  
    const updatedFormData = {
      ...(formData || {}),
      incidents: {
        ...(formData?.incidents || {}),
        injured_diagram: {
          ...(formData?.incidents?.injured_diagram || {}),
          image_url: "/human.jpg",
          marker_position: {
            x: Math.round(pixelX),
            y: Math.round(pixelY)
          }
        }
      }
    };
  
    setFormData(updatedFormData);
    localStorage.setItem(FORM_KEY, JSON.stringify(updatedFormData));
  };

  const handleImageLoad = (e: React.SyntheticEvent<HTMLImageElement>) => {
    const img = e.currentTarget;
    setImageSize({ width: img.clientWidth, height: img.clientHeight });
    console.log("Image loaded with size:", img.clientWidth, "x", img.clientHeight);
    
    const storedX = formData?.incidents?.injured_diagram?.marker_position?.x;
    const storedY = formData?.incidents?.injured_diagram?.marker_position?.y;
    
    if (storedX !== undefined && storedY !== undefined && !marker) {
      const normalizedX = storedX / img.clientWidth;
      const normalizedY = storedY / img.clientHeight;
      setMarker({ x: normalizedX, y: normalizedY });
    }
  };

  if (formData === null) return <p>Loading...</p>;

  // Create dynamic uiSchema based on current form values
  const createUiSchema = () => {
    const incidents = formData?.incidents || {};
    
    return {
      incidents: {
        // Hide other_incident_type unless incident_type is "Other"
        ...(incidents.incident_type !== "Other" && {
          other_incident_type: {
            "ui:widget": "hidden"
          }
        }),
        
        // Hide other_incident_category unless incident_category is "Other"
        ...(incidents.incident_category !== "Other" && {
          other_incident_category: {
            "ui:widget": "hidden"
          }
        }),
        
        // Hide other_nature_of_injury unless nature_of_injury is "Other"
        ...(incidents.nature_of_injury !== "Other" && {
          other_nature_of_injury: {
            "ui:widget": "hidden"
          }
        }),
        
        // Hide other_injured_body_part unless injured_body_part is "Other"
        ...(incidents.injured_body_part !== "Other" && {
          other_injured_body_part: {
            "ui:widget": "hidden"
          }
        }),
        
        // File upload widgets
        image_upload: { 
          "ui:widget": "FileUploadWidget",
        }
      },
      
        injuredPersons: {
        // Hide employment_type_other unless employment_type is "Other"
        ...(formData?.injuredPersons?.employment_type !== "Other" && {
          employment_type_other: {
            "ui:widget": "hidden"
          }
        }),
        
        // Hide shift_schedule_time unless shift_schedule is true
        ...(formData?.injuredPersons?.shift_schedule !== true && {
          shift_schedule_time: {
            "ui:widget": "hidden"
          }
        })
      },
      
      
      additional: {
        selectedOptions: {
          "ui:widget": "MultiSelectWidget"
        }
      }
    };
  };

  return (
    <div className="form-container" style={{ 
      maxWidth: '1200px', 
      margin: '0 auto', 
      padding: '2rem',
      backgroundColor: 'var(--background)',
      color: 'var(--foreground)'
    }}>
      <div className="form-header" style={{
        textAlign: 'center',
        marginBottom: '2rem',
        paddingBottom: '1rem',
        borderBottom: '2px solid #e0e0e0'
      }}>
        <h1 style={{
          fontSize: '2.5rem',
          fontWeight: '700',
          margin: '0',
          color: 'var(--foreground)'
        }}>Incident Reporting Form</h1>
        <p style={{
          fontSize: '1.1rem',
          color: '#666',
          marginTop: '0.5rem'
        }}>Please fill out all required fields to submit your incident report</p>
      </div>

      <div className="body-diagram-section" style={{
        backgroundColor: 'var(--background)',
        border: '1px solid #e0e0e0',
        borderRadius: '12px',
        padding: '1.5rem',
        marginBottom: '2rem',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <h3 style={{
          fontSize: '1.3rem',
          fontWeight: '600',
          marginBottom: '1rem',
          color: 'var(--foreground)'
        }}>Body Injury Location</h3>
        <p style={{
          fontSize: '0.9rem',
          color: '#666',
          marginBottom: '1rem'
        }}>Click on the body diagram to mark the location of injury</p>
        
        <div style={{ 
          position: "relative", 
          display: "inline-block", 
          marginBottom: '1rem',
          border: '2px dashed #ccc',
          borderRadius: '8px',
          padding: '10px'
        }}>
          <img
            src="/human.jpg"
            alt="Human body diagram for injury location"
            style={{ 
              width: '100%', 
              maxWidth: '500px', 
              height: 'auto', 
              cursor: "crosshair",
              borderRadius: '6px'
            }}
            onClick={handleImageClick}
            onLoad={handleImageLoad}
          />

          {marker && (
            <div
              style={{
                position: "absolute",
                top: `${marker.y * 100}%`,
                left: `${marker.x * 100}%`,
                transform: "translate(-50%, -50%)",
                color: "#ff4444",
                fontWeight: "bold",
                fontSize: '24px',
                pointerEvents: "none",
                textShadow: "2px 2px 4px rgba(255,255,255,0.8)",
                filter: 'drop-shadow(0 0 3px rgba(255,68,68,0.6))'
              }}
            >
              ✖
            </div>
          )}
        </div>

        {/* Display current coordinates */}
        {formData?.incidents?.injured_diagram?.marker_position?.x !== undefined && 
         formData?.incidents?.injured_diagram?.marker_position?.y !== undefined && (
          <div style={{ 
            padding: '1rem', 
            backgroundColor: '#f0f9ff', 
            border: '1px solid #bae6fd',
            borderRadius: '8px',
            fontSize: '0.9rem'
          }}>
            <strong style={{ color: '#0369a1' }}>✓ Injury Location Selected:</strong>
            <span style={{ marginLeft: '10px' }}>
              X: {formData.incidents.injured_diagram.marker_position.x}, 
              Y: {formData.incidents.injured_diagram.marker_position.y}
            </span>
            {imageSize && (
              <span style={{ marginLeft: '10px', color: '#666', fontSize: '0.8rem' }}>
                (Image: {imageSize.width} × {imageSize.height}px)
              </span>
            )}
          </div>
        )}
      </div>

      <div className="form-section" style={{
        backgroundColor: 'var(--background)',
        border: '1px solid #e0e0e0',
        borderRadius: '12px',
        padding: '2rem',
        marginBottom: '2rem',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <Form
          schema={reportingFormSchema}
          validator={validator}
          formData={formData}
          onChange={handleChange}
          onSubmit={handleSubmit}
          widgets={{
            FileUploadWidget,
            MultiSelectWidget, // FIX: Register the MultiSelectWidget
          }}
          uiSchema={createUiSchema()}
          className="custom-form"
          onError={(errors) => {
              console.log("Validation errors:", errors);
          }}
        />
      </div>

      <div className="form-actions" style={{
        display: 'flex',
        gap: '1rem',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '1.5rem',
        backgroundColor: 'var(--background)',
        border: '1px solid #e0e0e0',
        borderRadius: '12px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <button 
          onClick={handleReset}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: '#ef4444',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '1rem',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}
          onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#dc2626'}
          onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#ef4444'}
        >
           Reset Form
        </button>
        
        <Link 
          href="/"
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: '#6b7280',
            color: 'white',
            borderRadius: '8px',
            fontSize: '1rem',
            fontWeight: '600',
            textDecoration: 'none',
            transition: 'all 0.2s ease',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            display: 'inline-block'
          }}
        >
           Go Home
        </Link>
      </div>
    </div>
  );
}