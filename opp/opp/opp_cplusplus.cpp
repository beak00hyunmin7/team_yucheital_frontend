#include <iostream>

using namespace std;

enum { MAKE = 1, DEPOSIT, WITHDRAW, INQUIRE, EXIT };

char name[100];
int account_num[100];
int money = 0;


int Menu(void);
void MakeAccount();

int main(void) {
	int ans;
	while (1) {
		ans = Menu();
		switch (ans)
		{
			case(MAKE) {
				MakeAccount()
			}
		}
	}
}

int Menu(void) {
	int answer;
	cout << "-----Menu-----" << endl;
	cout << "1. 계좌개설" << endl;
	cout << "2. 입 금" << endl;
	cout << "3. 출 금" << endl;
	cout << "4. 계좌정보 전체 출력" << endl;
	cout << "5, 프로그램 종료" << endl;
	cout << "선택: ";
	cin >> answer;
	return answer;
}

void MakeAccuont(void) {
	cout << "[계좌개설]" << endl;
	cout << "계좌ID: ";
	cin >> account_id;
}