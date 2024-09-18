   import { render, screen, waitFor } from '@testing-library/react';
   import Dashboard from '../components/Dashboard';

   // Mock fetch
   global.fetch = jest.fn(() =>
     Promise.resolve({
       ok: true,
       json: () => Promise.resolve({ cpu: 50, memory: 60 }),
     })
   ) as jest.Mock;

   describe('Dashboard', () => {
     it('renders dashboard metrics', async () => {
       render(<Dashboard />);

       await waitFor(() => {
         expect(screen.getByText(/System Metrics/i)).toBeInTheDocument();
         expect(screen.getByText(/"cpu": 50/i)).toBeInTheDocument();
         expect(screen.getByText(/"memory": 60/i)).toBeInTheDocument();
       });
     });

     it('handles error when fetching metrics fails', async () => {
       (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('API error'));

       render(<Dashboard />);

       await waitFor(() => {
         expect(screen.getByText(/Failed to load metrics/i)).toBeInTheDocument();
       });
     });
   });