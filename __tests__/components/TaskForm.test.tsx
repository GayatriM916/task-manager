import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react-native';
import { TaskForm } from '../../src/components/TaskForm';

describe('TaskForm', () => {
  it('llama a onSubmit con el título ingresado al presionar "Guardar"', async () => {
    const mockOnSubmit = jest.fn();
    await render(<TaskForm onSubmit={mockOnSubmit} />);

    await fireEvent.changeText(
      screen.getByPlaceholderText('Escribe el título de la tarea'),
      'Mi nueva tarea'
    );
    await fireEvent.press(screen.getByText('Guardar'));

    expect(mockOnSubmit).toHaveBeenCalledWith('Mi nueva tarea');
  });

  it('no llama a onSubmit si el campo está vacío', async () => {
    const mockOnSubmit = jest.fn();
    await render(<TaskForm onSubmit={mockOnSubmit} />);

    await fireEvent.press(screen.getByText('Guardar'));

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});

describe('TaskForm - interfaz con consultas accesibles', () => {
  it('usa getByTestId y getByRole para simular changeText y press', async () => {
    const mockOnSubmit = jest.fn();
    await render(<TaskForm onSubmit={mockOnSubmit} />);

    await fireEvent.changeText(screen.getByTestId('input-titulo'), 'Tarea desde testID');
    await fireEvent.press(screen.getByRole('button', { name: 'Guardar' }));

    expect(mockOnSubmit).toHaveBeenCalledWith('Tarea desde testID');
  });

  it('consulta el botón con getByText y no envía si el input sigue vacío', async () => {
    const mockOnSubmit = jest.fn();
    await render(<TaskForm onSubmit={mockOnSubmit} />);

    expect(screen.getByTestId('input-titulo')).toBeTruthy();
    await fireEvent.press(screen.getByText('Guardar'));

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
