import { JSONSchema7 } from "json-schema";

export const reportingFormSchema: JSONSchema7 = {
  title: "Reporting Forms",
  type: "object",
  required: ["incidents", "injuredPersons", "medicalInfo", "witnessInfo"],
  properties: {
    incidents: {
      type: "object",
      required: [
        "business_unit", "site_name", "date_of_incident", "time_of_incident", "location",
        "description", "incident_type", "incident_category", "nature_of_injury",
        "injured_body_part", "injured_diagram"
      ],
      properties: {
        business_unit: { type: "string", minLength: 1, title: "Business Unit" },
        site_name: { type: "string", minLength: 1 ,title:"Site Name"},
        date_of_incident: { type: "string", format: "date", minLength: 1, title: "Date of Incident" },
        time_of_incident: { type: "string", format: "time", minLength: 1 ,title: "Time of Incident" },
        location: { type: "string", minLength: 1 ,title: "Location of Incident" },
        description: { type: "string", minLength: 1 ,title: "Description of Incident" },

        incident_type: {
          type: "string",
          enum: ["Health & Safety", "Environment", "Equipment & Infrastructure", "Security", "Other"],
          title: "Incident Type"
        },
        other_incident_type: { type: "string", minLength: 1 , title: "Other Incident Type" },

        incident_category: {
          type: "string",
          enum: [
            "First aid", "Near Miss", "Dangerous Occurrence", "Environmental Incident", "Fatal",
            "Security Impact", "Occupational Illness", "Other",
            "Lost Time Injury (Bodily Injury – Schedule 1)",
            "Lost Time Injury (Other than Bodily Injury – Schedule 1)"
          ],
          title: "Incident Category"
        },
        other_incident_category: { type: "string", minLength: 1 ,title: "Other Incident Category" },

        nature_of_injury: {
          type: "string",
          enum: [
            "Sprain/Strain", "Fracture", "Unconciousness", "Bruise", "Cut/Leceration",
            "Electric Shock", "Dislocation", "Other", "Burns", "Crushing", "Amputation"
          ],
          title: "Nature of Injury"
        },
        other_nature_of_injury: { type: "string", minLength: 1 ,title: "Other Nature of Injury" },

        injured_body_part: {
          type: "string",
          enum: ["Head", "Face", "Neck", "Arm", "Foot", "Toe", "Eye", "Leg", "Hand", "Other", "Finger"],
          title: "Injured Body Part"
        },
        other_injured_body_part: { type: "string", minLength: 1, title: "Other Injured Body Part" },

        injured_diagram: {
          type: "object",
          required: ["image_url", "marker_position"],
          title: "Injured Diagram",
          properties: {
            image_url: { type: "string", format: "uri", minLength: 1 , title: "Image URL" },
            marker_position: {
              type: "object",
              required: ["x", "y"],
              properties: {
                x: { type: "number" },
                y: { type: "number" }
              },
              title: "Marker Position",
            }
          }
        },
        image_upload: {
          type: "array",            
          title: "Incident Image Upload",
          items: {
            type: "string",         
            format: "data-url"
          }
        }
      },
      dependencies: {
        incident_type: {
          oneOf: [
            {
              properties: {
                incident_type: { const: "Other" },
                other_incident_type: { type: "string", minLength: 1 }
              },
              required: ["other_incident_type"]
            },
            {
              not: {
                properties: {
                  incident_type: { const: "Other" }
                }
              },
              required: []
            }
          ]
        },
        incident_category: {
          oneOf: [
            {
              properties: {
                incident_category: { const: "Other" },
                other_incident_category: { type: "string", minLength: 1 }
              },
              required: ["other_incident_category"]
            },
            {
              not: {
                properties: {
                  incident_category: { const: "Other" }
                }
              },
              required: []
            }
          ]
        },
        nature_of_injury: {
          oneOf: [
            {
              properties: {
                nature_of_injury: { const: "Other" },
                other_nature_of_injury: { type: "string", minLength: 1 }
              },
              required: ["other_nature_of_injury"]
            },
            {
              not: {
                properties: {
                  nature_of_injury: { const: "Other" }
                }
              },
              required: []
            }
          ]
        },
        injured_body_part: {
          oneOf: [
            {
              properties: {
                injured_body_part: { const: "Other" },
                other_injured_body_part: { type: "string", minLength: 1 }
              },
              required: ["other_injured_body_part"]
            },
            {
              not: {
                properties: {
                  injured_body_part: { const: "Other" }
                }
              },
              required: []
            }
          ]
        }
      }
    },

    injuredPersons: {
      type: "object",
      required: [
        "name", "designation", "department", "age", "immediate_supervisor", "employment_type",
        "period_work_in_sunway", "employment_start_date", "engaged_in_performing_task_related_to_incident",
        "period_task_related_to_incident", "shift_schedule"
      ],
      title: "Injured Persons Information",
      properties: {
        name: { type: "string", minLength: 1, title: "Name of Injured Person" },
        designation: { type: "string", minLength: 1 ,title: "Designation of Injured Person" },
        department: { type: "string", minLength: 1 ,title: "Department of Injured Person" },
        age: { type: "integer", minimum: 0 ,title: "Age of Injured Person" },
        immediate_supervisor: { type: "string", minLength: 1, title: "Immediate Supervisor" },

        employment_type: {
          type: "string",
          enum: ["Sunway", "Client", "Contractor", "Other"],
          title: "Employment Type"
        },
        employment_type_other: { type: "string", minLength: 1 },

        period_work_in_sunway: {
          type: "string",
          enum: ["<6months", "<6months - 1 year", "1-3 years", ">3 years"],
          title: "Period of Work in Sunway"
        },

        employment_start_date: { type: "string", format: "date", title: "Employment Start Date" },

        engaged_in_performing_task_related_to_incident: {
          type: "string", minLength: 1, title: "Engaged in Performing Task Related to Incident"
        },

        period_task_related_to_incident: {
          type: "string",
          enum: ["<6months", "<6months - 1 year", "1-3 years", ">3 years"],
          title: "Period of Task Related to Incident"
        },

        shift_schedule: { type: "boolean" , title: "Shift Schedule" },
        shift_schedule_time: {
          type: "string",
          enum: ["day", "afternoon", "night"],
          title: "Shift Schedule Time"
        }
      },
      dependencies: {
        employment_type: {
          oneOf: [
            {
              properties: {
                employment_type: { const: "Other" },
                employment_type_other: { type: "string", minLength: 1 }
              },
              required: ["employment_type_other"]
            },
            {
              not: {
                properties: {
                  employment_type: { const: "Other" }
                }
              },
              required: []
            }
          ]
        },
        shift_schedule: {
          oneOf: [
            {
              properties: {
                shift_schedule: { const: true },
                shift_schedule_time: { type: "string", enum: ["day", "afternoon", "night"] }
              },
              required: ["shift_schedule_time"]
            },
            {
              not: {
                properties: {
                  shift_schedule: { const: true }
                }
              },
              required: []
            }
          ]
        }
      }
    },

    medicalInfo: {
      type: "object",
      required: [
        "hospital", "med_cert_start_date", "med_cert_end_date", "med_cert_days",
        "ward_admitted_start_date", "ward_admitted_end_date", "ward_admitted_days"
      ],
      title: "Medical Information",
      properties: {
        hospital: { type: "string", minLength: 1 ,title: "Hospital Name" },
        med_cert_start_date: { type: "string", format: "date" ,title: "Medical Certificate Start Date" },
        med_cert_end_date: { type: "string", format: "date" ,title: "Medical Certificate End Date" },
        med_cert_days: { type: "integer", minimum: 0, title: "Medical Certificate Days" },
        ward_admitted_start_date: { type: "string", format: "date", title: "Ward Admitted Start Date" },
        ward_admitted_end_date: { type: "string", format: "date" ,title: "Ward Admitted End Date" },
        ward_admitted_days: { type: "integer", minimum: 0,  title: "Ward Admitted Days" },
        disability: {
          type: "string",
          enum: ["Permanent Disability", "Non-Permanent Disability"],
          title: "Disability Type"
        }
      }
    },

    witnessInfo: {
      type: "object",
      required: ["name", "designation", "witness_statement"],
      properties: {
        name: { type: "string", minLength: 1, title: "Witness Name" },
        designation: { type: "string", minLength: 1, title: "Witness Designation" },
        witness_statement: { type: "string", minLength: 1 ,title: "Witness Statement" },
      },
      title: "Witness Information",
    },

    additional : {
      "type": "object",
      "properties": {
        "selectedOptions": {
          "type": "array",
          "title": "Select Multiple Options",
          "minItems": 1,
          "items": {
            "type": "string",
            "enum": ["Option A", "Option B", "Option C", "Option D"],
          },
          "uniqueItems": true
        }
      }
    },
    
    email :{
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "title": "Email",
          "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        }
      },
      "required": ["email"]
    }
  },
};