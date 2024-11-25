import random


def generate_zipf_list(size: int) -> tuple:
    return tuple(str(i) for i in range(1, size + 1))


def generate_options(list: tuple, index_range: tuple[int, int]) -> tuple:
    sub_list = list[min(index_range) : max(index_range)]
    random_words = tuple(random.sample(sub_list, 8))
    pseudo_words = tuple(random.sample(["A", "B", "C", "D", "E", "F", "G", "H"], 8))
    options = []
    responses: list[bool] = []

    for i in range(8):
        pseudo_word = pseudo_words[i]
        random_word = random_words[i]
        select_real_word = random.choice([True, False])
        options.append(
            str(i + 1)
            + '. "'
            + (random_word if select_real_word else pseudo_word)
            + '"'
        )
        if select_real_word:
            responses.append(i)
    # delete the cases where total real words and total pseudo words are not 0
    # so we never divide by 0
    if not 0 < len(responses) < 8:
        return generate_options(list, index_range)
    return tuple(options), tuple(responses)


def get_score(user_response: tuple, responses: tuple) -> int:
    print(responses, user_response)
    total_real_words = len(responses)
    real_words_found = len([i for i in responses if i in user_response])
    hit_rate = real_words_found / total_real_words
    print(
        "Total real words: ",
        total_real_words,
        "Real words found: ",
        real_words_found,
        "Hit rate: ",
        hit_rate,
    )
    total_pseudo_words = 8 - total_real_words
    false_alarm_count = len(user_response) - real_words_found
    false_alarm_rate = false_alarm_count / total_pseudo_words
    print(
        "Total pseudo words: ",
        total_pseudo_words,
        "False alarms: ",
        false_alarm_count,
        "False alarm rate: ",
        false_alarm_rate,
    )
    if false_alarm_rate >= hit_rate:
        return 0
    a = 4 * hit_rate * (1 - false_alarm_rate)
    b = (hit_rate - false_alarm_rate) * (1 + hit_rate - false_alarm_rate)

    score_isdt = 1 - ((a - 2 * b) / (a - b))
    return score_isdt


def get_next_index_range(
    score: int, index_range: tuple[int, int], has_failed_once: bool
) -> tuple[int, int]:
    if has_failed_once:
        middle_index = round((index_range[0] + index_range[1]) / 2)
        if score < 0.5:
            return (min(index_range), middle_index)
        else:
            return (middle_index, max(index_range))
    else:
        return (max(index_range), int(max(index_range) * random.uniform(1.8, 2.4)))


def recursive_prompt(
    zipf_list: tuple, index_range: tuple[int, int], has_failed_before: bool
):
    options, responses = generate_options(zipf_list, index_range)
    for item in options:
        print(item)

    raw_input = input(
        "Enter the ids of the real words separated by commas (e.g: 1, 2, 3): "
    ).strip()
    user_response = tuple(
        [int(x.strip()) - 1 for x in raw_input.split(",")] if raw_input else []
    )
    score = get_score(user_response, responses)
    print("isdt score: ", score)
    failed_once = has_failed_before or score < 0.5

    next_index_range = get_next_index_range(score, index_range, failed_once)

    if max(next_index_range) - min(next_index_range) <= 8:
        print("Congratulations! You've reached index: ", max(next_index_range))
        return
    else:
        print("Next index: ", next_index_range)
        recursive_prompt(zipf_list, next_index_range, failed_once)


def main():
    zipf_list = generate_zipf_list(10000)

    print("\nStarting recursive prompt program...")
    recursive_prompt(zipf_list, (0, 10), False)


if __name__ == "__main__":
    main()
