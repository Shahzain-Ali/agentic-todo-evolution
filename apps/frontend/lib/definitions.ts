/**
 * Type definitions for the Todo application
 */

export type TaskStatus = 'pending' | 'completed';

export interface Task {
  id: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
  user_id: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: TaskStatus;
}

export interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}
