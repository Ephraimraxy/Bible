import { z } from 'zod';
import { verses } from './schema';

export const api = {
  sync: {
    method: 'GET' as const,
    path: '/api/sync' as const,
    responses: {
      200: z.array(z.custom<typeof verses.$inferSelect>()),
    },
  },
};

export function buildUrl(path: string, params?: Record<string, string | number>): string {
  let url = path;
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (url.includes(`:${key}`)) {
        url = url.replace(`:${key}`, String(value));
      }
    });
  }
  return url;
}
