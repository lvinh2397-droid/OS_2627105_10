
def banker():
    print("\n=== THUAT TOAN BANKER ===")

    # Moi hang tuong ung voi mot tien trinh P0, P1,...
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    maximum = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    available = [3, 3, 2]
    n = len(allocation)
    m = len(available)

    need = [
        [maximum[i][j] - allocation[i][j]
         for j in range(m)]
        for i in range(n)
    ]

    print("Ma tran Need = Max - Allocation:")
    for i, row in enumerate(need):
        print(f"P{i}: {row}")

    work = available.copy()
    finish = [False] * n
    safe_sequence = []

    while True:
        found = False

        for i in range(n):
            if not finish[i] and all(
                need[i][j] <= work[j] for j in range(m)
            ):
                for j in range(m):
                    work[j] += allocation[i][j]

                finish[i] = True
                safe_sequence.append(i)
                found = True

        if not found:
            break

    if all(finish):
        sequence = " -> ".join(
            f"P{i}" for i in safe_sequence
        )
        print("Trang thai AN TOAN")
        print("Thu tu an toan:", sequence)
    else:
        print("Trang thai KHONG AN TOAN")
        print("Khong tim duoc thu tu an toan.")


def detect_deadlock(allocation, request, available, active):
    n = len(allocation)
    m = len(available)

    work = available.copy()
    finish = []

    # Tien trinh khong giu tai nguyen co the xem la da ket thuc
    for i in range(n):
        has_resource = any(x > 0 for x in allocation[i])
        finish.append(not active[i] or not has_resource)

    changed = True

    while changed:
        changed = False

        for i in range(n):
            if active[i] and not finish[i]:
                can_finish = all(
                    request[i][j] <= work[j]
                    for j in range(m)
                )

                if can_finish:
                    for j in range(m):
                        work[j] += allocation[i][j]

                    finish[i] = True
                    changed = True

    return [
        i for i in range(n)
        if active[i] and not finish[i]
    ]


def show_deadlock(deadlocked):
    if deadlocked:
        names = ", ".join(f"P{i}" for i in deadlocked)
        print("Phat hien Deadlock tai:", names)
    else:
        print("Khong phat hien Deadlock.")


def deadlock_demo(recover=False):
    print("\n=== PHAT HIEN DEADLOCK ===")

    # Hai tien trinh giu hai tai nguyen khac nhau
    allocation = [
        [1, 0],  # P0 giu A
        [0, 1]   # P1 giu B
    ]

    request = [
        [0, 1],  # P0 doi B
        [1, 0]   # P1 doi A
    ]

    available = [0, 0]
    active = [True, True]

    if not recover:
        # Tinh huong khong Deadlock: P0 khong can them tai nguyen
        request[0] = [0, 0]

    deadlocked = detect_deadlock(
        allocation, request, available, active
    )
    show_deadlock(deadlocked)

    if not recover or not deadlocked:
        return

    print("\n=== PHUC HOI DEADLOCK ===")

    # Mo phong ket thuc tien trinh dau tien bi Deadlock
    victim = deadlocked[0]
    print(f"Ket thuc tien trinh P{victim}")

    # Thu hoi tai nguyen tien trinh dang giu
    for j in range(len(available)):
        available[j] += allocation[victim][j]
        allocation[victim][j] = 0
        request[victim][j] = 0

    active[victim] = False

    print("Tai nguyen san co sau phuc hoi:", available)

    deadlocked = detect_deadlock(
        allocation, request, available, active
    )

    print("Kiem tra lai sau phuc hoi:")
    show_deadlock(deadlocked)

    if not deadlocked:
        print("Phuc hoi thanh cong trong mo phong.")


def main():
    while True:
        print("\n==============================")
        print(" MO PHONG BANKER VA DEADLOCK")
        print("==============================")
        print("1. Chay thuat toan Banker")
        print("2. Phat hien Deadlock (khong co)")
        print("3. Phat hien va phuc hoi Deadlock")
        print("0. Thoat")

        choice = input("Nhap lua chon: ").strip()

        if choice == "1":
            banker()
        elif choice == "2":
            deadlock_demo(False)
        elif choice == "3":
            deadlock_demo(True)
        elif choice == "0":
            print("Ket thuc chuong trinh.")
            break
        else:
            print("Lua chon khong hop le!")


if __name__ == "__main__":
    main()
