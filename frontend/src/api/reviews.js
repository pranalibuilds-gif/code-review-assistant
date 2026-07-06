import client from './client';

export const getReviews = (params) =>
  client.get('/reviews', { params });

export const getReview = (id) =>
  client.get(`/reviews/${id}`);

export const deleteReview = (id) =>
  client.delete(`/reviews/${id}`);
