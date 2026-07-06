import client from './client';

export const getProjects = () => client.get('/projects');
export const createProject = (data) => client.post('/projects', data);
