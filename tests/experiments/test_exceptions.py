# def test_exceptions():
#     bunch = []
#     for i in range(1, 6):
#         grape = {"single": i, "double": i * 2}
#         bunch.append(grape)
#     try:
#         clover = [grape['triple'] for grape in bunch]
#         print(clover)
#     except KeyError:
#         print("We expected to find a 'triple' key in bunch")
#     print(bunch)


if __name__ == "__main__":
    test_exceptions()
