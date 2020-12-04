use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;
use std::collections::HashMap;
use std::io::{Write};
use std::io::LineWriter;
use std::process::Command;
use rust_decimal::prelude::*;


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn generate_factor_base_list(factor_base_size: u64) -> std::vec::Vec<u64> {
	let mut fb_list: Vec<u64> = Vec::new();
	let mut prime_counter: u64 = 0;

    if let Ok(lines) = read_lines("./prim_2_24.txt") {
        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            if let Ok(line_content) = line {
            	let splitted = line_content.split(" ");
            	for n in splitted {
            		if prime_counter == factor_base_size {
            			return fb_list;
            		} else {
            			if let Ok(prime) = n.parse::<u64>() {
	            			fb_list.push(prime);
	            			prime_counter += 1;
            			}
            		}
            	}
            }
        }
    }

    return fb_list;
}

fn prime_factorization(mut n: u64, factor_base_list: &Vec<u64>) -> std::collections::HashMap<u64, u64> {
	let mut results = HashMap::new();

	for prime in factor_base_list.iter() {
		let mut prime_counter = 0;
		while n % *prime == 0 {
			n = n / *prime;
			prime_counter += 1;
		}

		if prime_counter != 0 {
			results.insert(*prime, prime_counter);
		}

		if n == 1 {
			break;
		}
	}

	if n != 1 {
		return HashMap::new();
	} else {
		return results
	}
}

fn generate_matrix_row(factorization: &std::collections::HashMap<u64, u64>, factor_base_list: &Vec<u64>) -> Vec<u64> {
	let mut new_row: Vec<u64> = Vec::new();
	for prime in factor_base_list.iter() {
		match factorization.get(prime) {
			Some(&count) => new_row.push(count % 2),
			_ => new_row.push(0)
		}
	}

	return new_row;
}

fn generate_r_values_and_matrix(factor_base_size: u64, factor_base_list: &Vec<u64>, given_number: u64) -> (Vec<(u64, std::collections::HashMap<u64, u64>)>, Vec<Vec<u64>>) {
	let mut r_values_factorized: Vec<(u64, std::collections::HashMap<u64, u64>)> = Vec::new();
	let mut matrix: Vec<Vec<u64>> = Vec::new();
	let mut r_values_stored = 0;

	for k in 2..factor_base_size + 5 {
		for j in 2..k+1	 {
			let r =  (((k * given_number) as f64).sqrt()).floor() as u64 + j;
			let r_modulo = r.pow(2) % given_number;

			if r_modulo > 1 {
				let factorization = prime_factorization(r_modulo, factor_base_list);

				if !factorization.is_empty() {
					let new_row = generate_matrix_row(&factorization, factor_base_list);
					//println!("{}, {}, {:?}", k, j, r);
					//println!("{:?}", factorization);
					//println!("{:?}", new_row);
					matrix.push(new_row);
					r_values_factorized.push((r, factorization));
					r_values_stored += 1;
				}
			}

			if r_values_stored >= factor_base_size {
				return (r_values_factorized, matrix);
			}
		}
	}

	return (r_values_factorized, matrix);
}

fn gaussian_elimination(matrix: Vec<Vec<u64>>) -> std::vec::Vec<std::vec::Vec<u64>> {
	let mut results = Vec::<Vec<u64>>::new();
	let m = matrix.len();
	if m == 0 {
		return results;
	}

	let n = matrix[0].len();

  	let ofile = File::create("matrix_input.txt")
                       .expect("unable to create file");

    let mut ofile = LineWriter::new(ofile);

    let preamble = format!("{} {}\n", m, n);
	ofile.write_all(preamble.as_bytes()).expect("error");

	for row in matrix {
		for el in row {
			let line = format!("{} ", el);			
			ofile.write_all(line.as_bytes()).expect("error");
		}
		ofile.write_all("\n".as_bytes()).expect("error");
	}

	Command::new(".\\GaussBin.exe")	
			.args(&["matrix_input.txt", "out.txt"])
			.output()
			.expect("Something went wrong running GaussBin.");

	let input = File::open("out.txt").expect("error reading output");
    let buffered = BufReader::new(input);

    for line in buffered.lines().skip(1) {
	    let vec:Vec<u64> = line.unwrap()
		        .split_whitespace()
		        .map(|s| s.parse().expect("parse error"))
		        .collect();
		results.push(vec);
    }
    return results;
}

fn find_gcd(solutions: Vec<Vec<u64>>, r_values: Vec<(u64, std::collections::HashMap<u64, u64>)>, given_number: u64) -> (u64, u64) {
	for solution in solutions {
		let mut x = Decimal::new(1);
		let mut y = Decimal::new(1);
		for (eq_number, matrix_value) in solution.iter().enumerate() {
			if *matrix_value == 1 {
				x *= r_values[eq_number].0 % given_number;
				for (prime, count) in r_values[eq_number].1 {
					y *= prime.pow(count as u32);
				}
			}
		}
	}
}

fn main() {
	let factor_base_size = 30;
	let given_number = 16637;
	let factor_base_list = generate_factor_base_list(factor_base_size);

	let (r_values, matrix) = generate_r_values_and_matrix(factor_base_size+2, &factor_base_list, given_number);
	let solutions = gaussian_elimination(matrix);
	let (factor_1, factor_2) = find_gcd(solutions, r_values, given_number);

    println!("{}, {}", factor_1, factor_2);
}