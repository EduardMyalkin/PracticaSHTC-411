#define V_MAX 1
#define PROBABILITY 0
#define TOTAL_CARS 6

#include <iostream>
#include <iomanip>
#include <ctime>

using namespace std;

bool random_slow_down () {		//	функция для "броска монеты" на замедление
	double chance = (double)rand() / RAND_MAX;
	return (chance < PROBABILITY);
}
void print_array (int *array) {
	for (int i = 0; i < TOTAL_CARS; i++) {
		cout << setw(3) << array[i];
	}
}
void shift_array (int *array) {	//	циклично сдвигает массив на 1 вправо
	int temp = array[TOTAL_CARS - 1];
	for (int i = TOTAL_CARS - 1; i > 0; i--) {
		array[i] = array[i-1];
	}
	array[0] = temp;
}

int main () {

	srand(time(0));

	int zero_passes = 0;
	int positions[TOTAL_CARS] = {0,5,10,15,20,25};
	int velocities[TOTAL_CARS];
	for (int i = 0; i < TOTAL_CARS; i++) { velocities[i] = 0; }

	cout << "t=0    ";
	print_array(positions);
	cout << "    ";
	print_array(velocities);
	cout << endl;

	for (int t = 1; t < 31; t++) {

		//	ускорение всех автомобилей на 1, если скорость не максимальная
		for (int i = 0; i < TOTAL_CARS; i++) {
			if (velocities[i] < V_MAX) {
				velocities[i]++;
			}
		}

		//	проверка на замедление, если впереди есть другой автомобиль
		for (int i = 0; i < TOTAL_CARS - 1; i++) {
			int front_cells = positions[i+1] - positions[i] - 1;
			if (velocities[i] > front_cells) {
				velocities[i] = front_cells;
			}
		}
		int last_front_cells = 29 - positions[TOTAL_CARS - 1] + positions[0];	//	отдельная обработка последнего автомобиля из-за зацикливания
		if (velocities[TOTAL_CARS - 1] > last_front_cells) {
			velocities[TOTAL_CARS - 1] = last_front_cells;
		}

		//	случайное замедление
		for (int i = 0; i < TOTAL_CARS; i++) {
			if (random_slow_down() and velocities[i] != 0) {
				velocities[i]--;
			}
		}

		//	движение
		for (int i = 0; i < TOTAL_CARS; i++) {
			positions[i] += velocities[i];
		}
		if (positions[TOTAL_CARS - 1] > 29) {	//	проверка на пересечение нулевой клетки
			zero_passes++;
			positions[TOTAL_CARS - 1] -= 30;
			shift_array(positions);
			shift_array(velocities);
		}

		//	вывод строки
		cout << "t=" << t;
		cout << (t >= 10 ? "   " : "    ");
		print_array(positions);
		cout << "    ";
		print_array(velocities);
		cout << "    ";
		cout << zero_passes;
		cout << endl;

	}

}
