# Name: Gannon Strand
# OSU Email: strandga@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: June 5th 2025
# Description: Class to represent a HashMap using Separate Chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Function to update the key/value pair in the hashmap.
        """
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity*2)
        index = self._hash_function(key) % self._capacity
        if index > self._capacity - 1:
            return
        node = self._buckets[index].contains(key)
        if node is None:
            # Inserts it if node is none increments size
            self._buckets[index].insert(key, value)
            self._size += 1
        else:
            # If not change the value and doesn't increment size
            node.value = value

    def resize_table(self, new_capacity: int) -> None:
        """
        Function to resize the underlying table.
        """
        if new_capacity < 1:
            return
        if self._is_prime(new_capacity) is False:
            # Makes it prime if it isn't
            new_capacity = self._next_prime(new_capacity)
        buckets = self._buckets
        new_array = DynamicArray()

        for x in range(new_capacity):
            # Makes a new array of linked lists
            new_array.append(LinkedList())

        self._buckets = new_array
        self._capacity = new_capacity
        self._size = 0

        for x in range(buckets.length()):
            # Inserts existing elements into new dynamic array.
            bucket = buckets.get_at_index(x)
            node = bucket._head
            while node is not None:
                self.put(node.key, node.value)
                node = node.next

    def table_load(self) -> float:
        """
        Function to return the table's load factor
        """
        load_factor = self._size / self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Function to return how many empty buckets there are.
        """
        counter = 0
        buckets = self._buckets
        for x in range(buckets.length()):
            # Checks if bucket is empty and adds it to a counter
            bucket = buckets.get_at_index(x)
            node = bucket._head
            if node is None:
                counter += 1
        return counter

    def get(self, key: str) -> object:
        """
        Function to return the value associated with a key
        """
        index = self._hash_function(key) % self._capacity
        node = self._buckets[index].contains(key)
        if node is None:
            return
        else:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        Function to check if the HashMap contains a key.
        """
        index = self._hash_function(key) % self._capacity
        node = self._buckets[index].contains(key)
        if node is None:
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        """
        Function to remove a value from the HashMap.
        """
        if self.contains_key(key) is False:
            return
        index = self._hash_function(key) % self._capacity
        self._buckets[index].remove(key)
        self._size -= 1
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Function to get keys and values of the hashmap in a DynamicArray.
        """
        new_array = DynamicArray()
        buckets = self._buckets
        for x in range(buckets.length()):
            # Inserts existing keys/values into new dynamic array.
            bucket = buckets.get_at_index(x)
            node = bucket._head
            while node is not None:
                new_array.append((node.key, node.value))
                node = node.next
        return new_array

    def clear(self) -> None:
        """
        Function to clear the hashmap.
        """
        self._buckets = DynamicArray()
        for x in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Function to find the mode of the hashmap.
    """
    map = HashMap()
    max_count = 0
    new_array = DynamicArray()
    for x in range(da.length()):
        value = map.get(da.get_at_index(x))
        if value is None:
            # If not in the array add it
            map.put(da.get_at_index(x), 1)
            value = 1
        else:
            # If in the array update the value
            value += 1
            map.put(da.get_at_index(x), value)

        if value > max_count:
            # Makes a new array and adds that value to the array
            new_array = DynamicArray()
            new_array.append(da.get_at_index(x))
            max_count = value

        elif value == max_count:
            # If it's the same adds that value to the array
            new_array.append(da.get_at_index(x))

    return new_array, max_count


# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
