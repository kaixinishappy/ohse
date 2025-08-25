// Allows uploading multiple image files at once.
// Accepts only image file types (jpeg, png, gif, webp, bmp, svg).
// Validates file type and size (max 10MB per file).
// Displays error messages for invalid files or upload errors.
// Shows a list of uploaded files with their names.
// Lets users delete individual uploaded files.
// Displays upload status and feedback (number of images uploaded).
// Converts files to base64 format for form submission.
// Updates the form data and internal state when files are added or removed.

import React from 'react';
import { WidgetProps } from '@rjsf/utils';

const FileUploadWidget: React.FC<WidgetProps> = ({
  id,
  value = [],
  onChange,
  options = {},
  label,
  required = false,
}) => {
  const [error, setError] = React.useState<string>('');
  const [files, setFiles] = React.useState<{ name: string; base64: string }[]>([]);

  const accept = 'image/*';
  const maxSize = 10 * 1024 * 1024; // 10MB

  React.useEffect(() => {
    // If value is externally reset, update internal files list
    if (value.length === 0) setFiles([]);
  }, [value]);

  const validateFile = (file: File): string | null => {
    const validTypes = [
      'image/jpeg', 'image/png', 'image/gif',
      'image/webp', 'image/bmp', 'image/svg+xml'
    ];
    if (!validTypes.includes(file.type)) {
      return `Invalid file type: ${file.type}`;
    }
    if (file.size > maxSize) {
      return `File "${file.name}" is too large (max 10MB).`;
    }
    return null;
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const filesInput = event.target.files;
    setError('');
    if (!filesInput || filesInput.length === 0) return;

    const validationErrors: string[] = [];
    const base64Promises: Promise<{ name: string; base64: string }>[] = [];

    Array.from(filesInput).forEach((file) => {
      const err = validateFile(file);
      if (err) {
        validationErrors.push(err);
      } else {
        base64Promises.push(
          new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () =>
              resolve({ name: file.name, base64: reader.result as string });
            reader.onerror = () => reject(`Failed to read "${file.name}"`);
            reader.readAsDataURL(file);
          })
        );
      }
    });

    if (validationErrors.length > 0) {
      setError(validationErrors.join('\n'));
      event.target.value = '';
      return;
    }

    Promise.all(base64Promises)
      .then((newFiles) => {
        const updatedFiles = [...files, ...newFiles];
        setFiles(updatedFiles);
        onChange(updatedFiles.map(f => f.base64)); 

      })
      .catch((err) => {
        setError(`${err}`);
      });
  };

  const handleRemove = (indexToRemove: number) => {
    const updated = files.filter((_, idx) => idx !== indexToRemove);
    setFiles(updated);
    onChange(updated.map(f => f.base64));
  };

  return (
    <div>
      <input
        id={id}
        type="file"
        accept={accept}
        multiple
        onChange={handleFileChange}
        style={{
          marginBottom: '10px',
          border: error ? '2px solid #ef4444' : '2px dashed #d1d5db',
          padding: '0.5rem',
          borderRadius: '6px',
          width: '100%',
        }}
      />

      {error && (
        <div style={{
          color: '#ef4444',
          backgroundColor: '#fef2f2',
          border: '1px solid #fecaca',
          borderRadius: '6px',
          padding: '0.75rem',
          marginBottom: '10px',
          fontSize: '0.875rem',
          whiteSpace: 'pre-line'
        }}>
          <strong>Upload Error:</strong><br />{error}
        </div>
      )}

      {files.length > 0 && !error && (
        <div style={{
          marginTop: '10px',
          backgroundColor: '#f0fdf4',
          border: '1px solid #bbf7d0',
          borderRadius: '6px',
          padding: '0.75rem'
        }}>
          <p style={{
            color: '#166534',
            marginBottom: '0.5rem',
            fontSize: '0.875rem'
          }}>
            ✅ {files.length} image(s) uploaded:
          </p>
          <ul style={{
            margin: 0,
            paddingLeft: '1rem',
            color: '#166534',
            fontSize: '0.875rem'
          }}>
            {files.map((file, idx) => (
              <li key={idx} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                {file.name}
                <button
                  type="button"
                  onClick={() => handleRemove(idx)}
                  style={{
                    marginLeft: '10px',
                    backgroundColor: '#ef4444',
                    color: 'white',
                    border: 'none',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '0.75rem',
                    fontWeight: 500
                  }}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FileUploadWidget;
