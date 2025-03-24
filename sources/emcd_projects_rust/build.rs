// vim: set filetype=rust fileencoding=utf-8:
// -*- coding: utf-8 -*-

/****************************************************************************
 *                                                                          *
 * Licensed under the Apache License, Version 2.0 (the "License");          *
 * you may not use this file except in compliance with the License.         *
 * You may obtain a copy of the License at                                  *
 *                                                                          *
 *     http://www.apache.org/licenses/LICENSE-2.0                           *
 *                                                                          *
 * Unless required by applicable law or agreed to in writing, software      *
 * distributed under the License is distributed on an "AS IS" BASIS,        *
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. *
 * See the License for the specific language governing permissions and      *
 * limitations under the License.                                           *
 *                                                                          *
 ****************************************************************************/


use std::fs::File;
use std::io::Read;
use std::path::PathBuf;
use regex::Regex;

fn main() {
    // Read Python package version
    let mut init_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    init_path.pop();  // up from emcd_projects_rust
    init_path.push("emcd_projects");
    init_path.push("__init__.py");

    // If not found, try the editable install layout
    if !init_path.exists() {
        init_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        init_path.pop();  // up from emcd_projects_rust
        init_path.pop();  // up from sources
        init_path.push("sources");
        init_path.push("emcd_projects");
        init_path.push("__init__.py");
    }

    let mut init_content = String::new();
    File::open(&init_path)
        .unwrap_or_else(|_| panic!("Failed to open __init__.py at {init_path:?}"))
        .read_to_string(&mut init_content)
        .expect("Failed to read __init__.py");

    // Extract version using regex
    let version_re = Regex::new(r#"__version__\s*=\s*['"]([^'"]+)['"]"#)
        .expect("Failed to compile version regex");

    if let Some(captures) = version_re.captures(&init_content) {
        let version = captures.get(1)
            .expect("No version capture group")
            .as_str();

        // Pass version to Rust compiler for use in lib.rs
        println!("cargo:rustc-env=CRATE_VERSION={version}");
    } else {
        panic!("Could not find __version__ in __init__.py");
    }
}
