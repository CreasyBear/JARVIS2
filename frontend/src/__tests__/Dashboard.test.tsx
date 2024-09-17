import { render, screen } from '@testing-library/react';
import Dashboard from '../components/Dashboard';

test('renders dashboard metrics', () => {
  render(<Dashboard />);
  const metricElement = screen.getByText(/system metrics/i);
  expect(metricElement).toBeInTheDocument();
});