import client from './client';

export const submitPaste = (data) => client.post('/submissions/paste', data);
export const submitUpload = (formData) => client.post('/submissions/upload', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
export const submitGithub = (data) => client.post('/submissions/github', data);

export const getSubmissionStatus = (id) => client.get(`/submissions/status/${id}`);
