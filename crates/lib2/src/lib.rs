#[no_mangle]
pub unsafe extern "C" fn modify_char(ptr: *mut libc::c_char) {
    *ptr = 'a' as libc::c_char;
}
