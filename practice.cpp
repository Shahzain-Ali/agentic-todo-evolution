Type convertion from current data type to another data type:

class Person{

    private:
        char* bufferptr:

    Person(int a){
        char array[15]
        itoa(a,array,10)
        size = strlen(array)
        bufferptr = new char[size + 1]
        strcpy(bufferptr,array)
    }

    char* getstringptr() const{
        return bufferptr
    }
}


Type convertion from  another data type to current data type:

class String {
    private:
        char* bufferPtr;
    public:
        String(const char* objValue = "") {
            size = strlen(objValue)
            bufferPtr = new char[size + 1];
            strcpy(bufferPtr, objValue);
        }

        // Conversion operator
        operator char*() const {
            return bufferPtr;
        }
};

int main() {
    String s("Hello");
    char* p = s;        // conversion from String → char*
    cout << p << endl;  // prints "Hello"
    return 0;
}


