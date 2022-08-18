use std::ffi::CString;

use once_cell::sync::Lazy;

#[no_mangle]
pub unsafe extern "C" fn version_as_heap_allocated_string() -> *const libc::c_char {
    return VERSION.as_ptr();

    static VERSION: Lazy<CString> = Lazy::new(|| CString::new(env!("CARGO_PKG_VERSION")).unwrap());
}

#[no_mangle]
pub static version_as_string_literal: &libc::c_char = {
    static VERSION: &str = concat!(env!("CARGO_PKG_VERSION"), '\0');
    unsafe { &*(&VERSION.as_bytes()[0] as *const u8 as *const libc::c_char) }
};
