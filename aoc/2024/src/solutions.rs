use crate::utils;

pub fn day1() {
    let input = utils::read_input(2024, 1).unwrap();
    let mut left_list: Vec<i32> = Vec::new();
    let mut right_list: Vec<i32> = Vec::new();

    for line in input.lines() {
        let nums: Vec<&str> = line.split_whitespace().collect();
        left_list.push(nums[0].parse().unwrap());
        right_list.push(nums[1].parse().unwrap());
    }

    left_list.sort();
    right_list.sort();

    let mut distance = 0;
    for it in left_list.iter().zip(right_list.iter()) {
        let (left, right) = it;
        distance += i32::abs(left - right);
    }
    utils::print_result(2024, 1, 1, distance.to_string());

    let mut similarity = 0;
    for num in left_list {
        let count = right_list.iter().filter(|&n| *n == num).count() as i32;
        similarity += num * count;
    }
    utils::print_result(2024, 1, 2, similarity.to_string());
}

pub fn day2() {
    fn is_unsafe(a: i32, b: i32, sign: i32) -> bool {
        (a - b).signum() != sign || a.abs_diff(b) == 0 || a.abs_diff(b) > 3
    }

    fn is_report_safe(levels: &Vec<i32>) -> bool {
        let sign = (levels[0] - levels[1]).signum();
        for i in 0..(levels.len() - 1) {
            if is_unsafe(levels[i], levels[i + 1], sign) {
                //println!("Report {:?} unsafe: {:?}[{:?}]", levels, levels[i], i);
                return false;
            }
        }
        //println!("Report {:?} safe", levels);
        true
    }

    let input = utils::read_input(2024, 2).unwrap();

    let mut safe_reports = 0;
    let mut dampener_safe_reports = 0;
    for line in input.lines() {
        let levels: Vec<i32> = line
            .split_whitespace()
            .map(|s| s.parse::<i32>().unwrap())
            .collect();

        if is_report_safe(&levels) {
            safe_reports += 1;
            dampener_safe_reports += 1;
        } else {
            let mut any_safe = false;
            for i in 0..levels.len() {
                let mut levels_clone = levels.clone();
                levels_clone.remove(i);
                if is_report_safe(&levels_clone) {
                    any_safe = true;
                    break;
                }
            }
            if any_safe {
                dampener_safe_reports += 1;
            }
        }
    }
    utils::print_result(2024, 2, 1, safe_reports.to_string());
    utils::print_result(2024, 2, 2, dampener_safe_reports.to_string());
}

pub fn day3() {
    use regex::Regex;

    let input = utils::read_input(2024, 3).unwrap();

    let re_do = Regex::new(r"(do(?:n\'t)?\(\))").unwrap();
    let re_mul = Regex::new(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)").unwrap();

    let mut result = 0;
    let mut result_do = 0;

    let mut left = 0;
    let mut right;
    let mut is_do = true;
    for cap in re_do.find_iter(&input) {
        // iterate over do's and dont's and parse for multiplications between them
        right = cap.start();
        for (_, [a, b]) in re_mul
            .captures_iter(&input[left..right])
            .map(|c| c.extract())
        {
            let mul_result = a.parse::<i32>().unwrap() * b.parse::<i32>().unwrap();
            result += mul_result;
            if is_do {
                result_do += mul_result;
            }
        }
        left = cap.end();
        is_do = cap.as_str() == "do()";
    }
    right = input.len() - 1;
    for (_, [a, b]) in re_mul
        .captures_iter(&input[left..right])
        .map(|c| c.extract())
    {
        let mul_result = a.parse::<i32>().unwrap() * b.parse::<i32>().unwrap();
        result += mul_result;
        if is_do {
            result_do += mul_result;
        }
    }
    utils::print_result(2024, 3, 1, result.to_string());
    utils::print_result(2024, 3, 2, result_do.to_string());
}

pub fn day4() {
    fn check_xmas(haystack: &str) -> i32 {
        if haystack.len() < 4 {
            return 0;
        }

        let mut total = 0;
        for i in 0..haystack.len() - 3 {
            if &haystack[i..i + 4] == "XMAS" || &haystack[i..i + 4] == "SAMX" {
                total += 1;
            }
        }
        total
    }

    let input = utils::read_input(2024, 4).unwrap();
    let mut input_matrix: Vec<Vec<char>> = Vec::new();
    for line in input.lines() {
        input_matrix.push(line.chars().collect());
    }
    let input_rows = input_matrix.len();
    let input_cols = input_matrix[0].len();

    let mut result = 0;
    // horizontal
    result += check_xmas(&input);

    // vertical
    for j in 0..input_cols {
        let mut temp_input = String::new();
        for i in 0..input_rows {
            temp_input.push(input_matrix[i][j]);
        }
        result += check_xmas(&temp_input);
    }

    // diagonals
    // starting in row 0
    for col in 0..input_cols {
        let mut temp_input = String::new();
        let mut i = 0;
        let mut j = col;
        while i < input_rows && j < input_cols {
            temp_input.push(input_matrix[i][j]);
            i += 1;
            j += 1;
        }
        result += check_xmas(&temp_input);
    }
    // starting in column 0 (except main diag)
    for row in 1..input_rows {
        let mut temp_input = String::new();
        let mut i = row;
        let mut j = 0;
        while i < input_rows && j < input_cols {
            temp_input.push(input_matrix[i][j]);
            i += 1;
            j += 1;
        }
        result += check_xmas(&temp_input);
    }

    // anti diagonals
    // starting in row 0
    for col in (0..input_cols).rev() {
        let mut temp_input = String::new();
        let mut i = 0;
        let mut j = col as i32;
        while i < input_rows && j >= 0 {
            temp_input.push(input_matrix[i][j as usize]);
            i += 1;
            j -= 1;
        }
        result += check_xmas(&temp_input);
    }
    // starting in column 0 (except main diag)
    for row in 1..input_rows {
        let mut temp_input = String::new();
        let mut i = row;
        let mut j = input_cols as i32 - 1;
        while i < input_rows && j >= 0 {
            temp_input.push(input_matrix[i][j as usize]);
            i += 1;
            j -= 1;
        }
        result += check_xmas(&temp_input);
    }

    utils::print_result(2024, 4, 1, result.to_string());
}
