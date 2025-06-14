# Name: Gannon Strand
# OSU Email: strandga@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: June 5th 2025
# Description: Function to represent a hashmap using Open Addressing with Quadratic Probing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Function to update the key/value pair.
        """
        if self.table_load() >= 0.5:
            new_capacity = self._capacity * 2
            if self._is_prime(new_capacity) is False:
                new_capacity = self._next_prime(new_capacity)
            self.resize_table(new_capacity)
        index = self._hash_function(key) % self._capacity
        x = 0
        tombstone_index = None
        while x < self._capacity:
            probe_index = (index + x * x) % self._capacity
            current = self._buckets[probe_index]

            if current is None:
                # If current is none/a tombstone it inserts a new key/value pair
                if tombstone_index is not None:
                    self._buckets[tombstone_index] = HashEntry(key, value)
                else:
                    self._buckets[probe_index] = HashEntry(key, value)
                self._size += 1
                return

            if current.is_tombstone:
                # Assigns a tombstone index in case key is not already in hashmap
                if tombstone_index is None:
                    tombstone_index = probe_index

            elif current.key == key:
                # Else it updates the value at that key
                current.value = value
                return
            x += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Function to resize the underlying table.
        """
        if new_capacity < self._size:
            return
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        buckets = self._buckets
        new_array = DynamicArray()

        for x in range(new_capacity):
            # Sets up new array with default none values.
            new_array.append(None)

        self._buckets = new_array
        self._capacity = new_capacity
        self._size = 0

        for x in range (buckets.length()):
            value = buckets[x]
            if value is not None and value.is_tombstone is False:
                # If value isn't a tombstone and not none inserts it.
                self.put(value.key, value.value)

    def table_load(self) -> float:
        """
        Function to get the HashMaps table load
        """
        load_factor = self._size / self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Function to return the number of empty buckets in the hashmap
        """
        counter = 0
        buckets = self._buckets
        for x in range(self._buckets.length()):
            value = buckets[x]
            if value is None:
                # If it's none add one to the counter.
                counter += 1

        return counter

    def get(self, key: str) -> object:
        """
        Function to get a value associated with a key
        """
        index = self._hash_function(key) % self._capacity
        x = 0
        while x < self._capacity:
            probe_index = (index + x * x) % self._capacity
            current = self._buckets[probe_index]

            if current is None:
                # If current is none it's not in the HashMap
                return None
            if current.key == key and current.is_tombstone is False:
                return current.value
            x += 1
        return None

    def contains_key(self, key: str) -> bool:
        """
        Function to check if a key is in the hashmap.
        """
        buckets = self._buckets
        for x in range(self._buckets.length()):
            value = buckets[x]
            if value is not None and value.is_tombstone is False and value.key == key:
                return True

        return False

    def remove(self, key: str) -> None:
        """
        Function to remove a key/value pair from the hashmap.
        """
        if self.contains_key(key) is False:
            return
        index = self._hash_function(key) % self._capacity
        x = 0
        while x < self._capacity:
            probe_index = (index + x * x) % self._capacity
            current = self._buckets[probe_index]

            if current is None:
                # If current is none it's not in the HashMap
                return
            if current.key == key and current.is_tombstone is False:
                current.is_tombstone = True
                self._size -= 1
                return

            x += 1
        return None

    def get_keys_and_values(self) -> DynamicArray:
        """
        Function to get all keys/values in a new DynamicArray
        """
        new_array = DynamicArray()
        buckets = self._buckets
        for x in range(buckets.length()):
            current = self._buckets[x]
            if current is not None and current.is_tombstone is False:
                # Adds the value if it exists and not a tombstone
                new_array.append((current.key, current.value))
        return new_array

    def clear(self) -> None:
        """
        Function to clear the HashMap.
        """
        new_array = DynamicArray()

        for x in range(self._capacity):
            # Sets up new array with default none values.
            new_array.append(None)

        self._buckets = new_array
        self._size = 0

    def __iter__(self):
        """
        Iterator for the HashMap
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain the next value and advance iterator
        """
        while self._index < self._buckets.length():
            value = self._buckets[self._index]
            self._index += 1
            if value is not None and value.is_tombstone is False:
                return value
        raise StopIteration


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
