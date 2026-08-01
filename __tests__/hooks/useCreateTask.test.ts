import { renderHook, act } from '@testing-library/react-native';
import { useCreateTask } from '../../src/hooks/useCreateTask';
import * as taskService from '../../src/services/taskService';

// Mock: aislamos taskService porque es una dependencia externa (capa de servicio).
// Así controlamos éxito/fallo de createTask sin depender de su implementación real
// (p. ej. red o Date.now) y verificamos el efecto secundario de la llamada.
jest.mock('../../src/services/taskService');

const mockedCreateTask = taskService.createTask as jest.MockedFunction<
  typeof taskService.createTask
>;

describe('useCreateTask', () => {
  beforeEach(() => {
    // Limpia historial e implementaciones de los jest.fn() del módulo mockeado
    // para que cada prueba defina su propio comportamiento de createTask.
    jest.clearAllMocks();
  });

  it('inicia en estado idle con la lista de tareas vacía', async () => {
    const { result } = await renderHook(() => useCreateTask());

    expect(result.current.status).toBe('idle');
    expect(result.current.tasks).toEqual([]);
  });

  it('crea una tarea exitosamente y actualiza el estado a success', async () => {
    // Mock: forzamos una respuesta exitosa controlada de createTask.
    mockedCreateTask.mockResolvedValue({
      id: '1',
      title: 'Estudiar Jest',
      status: 'pending',
    });

    const { result } = await renderHook(() => useCreateTask());

    await act(async () => {
      await result.current.submit('Estudiar Jest');
    });

    expect(mockedCreateTask).toHaveBeenCalledWith('Estudiar Jest');
    expect(result.current.status).toBe('success');
    expect(result.current.tasks).toHaveLength(1);
    expect(result.current.tasks[0].title).toBe('Estudiar Jest');
  });

  it('establece status en loading y luego en error si createTask falla', async () => {
    let rejectCreate: (reason?: unknown) => void;
    // Mock: diferimos el rechazo para observar el estado loading y luego el error.
    mockedCreateTask.mockImplementation(
      () =>
        new Promise((_, reject) => {
          rejectCreate = reject;
        })
    );

    const { result } = await renderHook(() => useCreateTask());

    let submitPromise: Promise<void>;
    await act(async () => {
      submitPromise = result.current.submit('Tarea fallida');
    });

    expect(result.current.status).toBe('loading');

    await act(async () => {
      rejectCreate!(new Error('Error de red'));
      await submitPromise;
    });

    expect(result.current.status).toBe('error');
    expect(result.current.tasks).toEqual([]);
  });

  it('elimina una tarea de la lista por su id', async () => {
    // Mock: proveemos una tarea con id fijo para poder llamar a removeTask después.
    mockedCreateTask.mockResolvedValue({
      id: '99',
      title: 'Tarea a eliminar',
      status: 'pending',
    });

    const { result } = await renderHook(() => useCreateTask());

    await act(async () => {
      await result.current.submit('Tarea a eliminar');
    });
    expect(result.current.tasks).toHaveLength(1);

    await act(() => {
      result.current.removeTask('99');
    });

    expect(result.current.tasks).toEqual([]);
  });
});
