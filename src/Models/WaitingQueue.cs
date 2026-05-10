namespace ClinicApp.Models;

public class WaitingQueue<T>
{
    private Queue<T> _queue = new Queue<T>();

    public int Count => _queue.Count;
    public bool IsEmpty => _queue.Count == 0;

    public void Enqueue(T item) => _queue.Enqueue(item);

    public T Dequeue()
    {
        if (IsEmpty) throw new InvalidOperationException("Черга порожня.");
        return _queue.Dequeue();
    }

    public T Peek()
    {
        if (IsEmpty) throw new InvalidOperationException("Черга порожня.");
        return _queue.Peek();
    }

    public T[] ToArray() => _queue.ToArray();
}
