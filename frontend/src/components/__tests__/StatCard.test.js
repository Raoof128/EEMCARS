import React from 'react';
import { render, screen } from '@testing-library/react';
import StatCard from '../StatCard';

describe('StatCard Component', () => {
  test('renders title and value', () => {
    render(<StatCard title="Total Assets" value="500" />);

    expect(screen.getByText('Total Assets')).toBeInTheDocument();
    expect(screen.getByText('500')).toBeInTheDocument();
  });

  test('renders with color prop', () => {
    const { container } = render(
      <StatCard title="Test" value="123" color="primary" />
    );

    // Check if card has proper styling
    expect(container.firstChild).toBeInTheDocument();
  });

  test('renders icon when provided', () => {
    const TestIcon = () => <span data-testid="test-icon">Icon</span>;
    render(<StatCard title="Test" value="123" icon={<TestIcon />} />);

    expect(screen.getByTestId('test-icon')).toBeInTheDocument();
  });

  test('handles large numbers', () => {
    render(<StatCard title="Test" value="1,234,567" />);

    expect(screen.getByText('1,234,567')).toBeInTheDocument();
  });

  test('renders subtitle when provided', () => {
    render(<StatCard title="Assets" value="500" subtitle="Total endpoints" />);

    expect(screen.getByText('Total endpoints')).toBeInTheDocument();
  });
});
