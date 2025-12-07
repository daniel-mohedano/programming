use colored::Colorize;
use reqwest::header::{HeaderMap, HeaderValue, COOKIE};
use std::env;
use std::fs;
use std::io::Write;
use std::path::Path;

static INPUT_DIR: &str = "inputs";

pub fn read_input(year: i32, day: i32) -> Result<String, Box<dyn std::error::Error>> {
    let dir_path = Path::new(INPUT_DIR);
    let file_path = dir_path.join(format!("{}.txt", day));

    if !dir_path.exists() {
        fs::create_dir_all(dir_path)?;
    }

    if !file_path.exists() {
        // Cache input
        let input = make_request(year, day)?;
        let mut file = fs::File::create(&file_path)?;
        file.write_all(input.as_bytes())?;
        Ok(input)
    } else {
        // Read input
        let input = fs::read_to_string(file_path)?;
        Ok(input)
    }
}

pub fn print_result(year: i32, day: i32, half: i32, result: String) {
    println!(
        "Result for [{}-{}-{}]: {}",
        year.to_string().yellow(),
        day.to_string().yellow(),
        half.to_string().yellow(),
        result.green()
    );
}

fn make_request(year: i32, day: i32) -> Result<String, Box<dyn std::error::Error>> {
    let uri: String = format!("https://adventofcode.com/{}/day/{}/input", year, day);
    let token_key = "AOC_TOKEN";
    let aoc_token = env::var(token_key)?;

    let client = reqwest::blocking::Client::new();
    let mut headers = HeaderMap::new();
    headers.insert(COOKIE, HeaderValue::from_str(&aoc_token)?);
    println!("{}{}", "Making request to: ".red(), uri.red());
    let response = client.get(uri).headers(headers).send()?;
    Ok(response.text().unwrap())
}
