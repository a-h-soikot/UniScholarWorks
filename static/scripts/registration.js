
const emailInput = document.getElementById('email');
const emailFeedback = document.getElementById('email-feedback');
const requestOtpBtn = document.getElementById('request-otp');
const otpWrapper = document.getElementById('otp-input-wrapper');
const otpInput = document.getElementById('otp');
const otpFeedback = document.getElementById('otp-feedback');
const otpStatus = document.getElementById('otp-status');
const verifyOtpBtn = document.getElementById('verify-otp');
const studentIdInput = document.getElementById('student_id');
const studentIdFeedback = document.getElementById('student-id-feedback');
const passwordInput = document.getElementById('password');
const passwordFeedback = document.getElementById('password-feedback');
const confirmPasswordInput = document.getElementById('confirm_password');
const confirmPasswordFeedback = document.getElementById('confirm-password-feedback');
const registerBtn = document.getElementById('register');
const form = document.querySelector('form');

let otpVerified = false;
let emailAvailable = false;
let studentIdValid = false;
let studentIdAvailable = false;
let passwordValid = false;
let passwordsMatch = false;
let resendTimer = null;
let latestEmailCheck = 0;
let latestStudentIdCheck = 0;
let lastEmailCheckedValue = '';
let lastStudentIdCheckedValue = '';
let lastEmailAvailability = null;
let lastStudentIdAvailability = null;

const EMAIL_DOMAIN_REGEX = /^[^@\s]+@student\.nstu\.edu\.bd$/i;
const PASSWORD_REGEX = /^(?=.*\d)(?=.*\D).{8,}$/;
const STUDENT_ID_REGEX = /^[A-Z]{3}\d{7}[MF]$/;

const setHelperText = (element, message = '', type = 'info') => {
    if (!element) return;
    element.textContent = message;
    element.classList.remove('error-text', 'success-text', 'info-text');
    if (message) {
        if (type === 'error') {
            element.classList.add('error-text');
        } else if (type === 'success') {
            element.classList.add('success-text');
        } else {
            element.classList.add('info-text');
        }
    }
};

const checkAvailability = async (field, value) => {
    const response = await fetch('/check_availability', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin',
        body: JSON.stringify({ field, value })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || 'Unable to check availability right now.');
    }

    return !data.exists;
};

const handleEmailAvailability = async () => {
    const email = emailInput.value.trim();
    if (!validateEmail()) {
        emailAvailable = false;
        lastEmailCheckedValue = '';
        lastEmailAvailability = null;
        updateRegisterButtonState();
        return false;
    }

    if (email === lastEmailCheckedValue && lastEmailAvailability !== null) {
        emailAvailable = lastEmailAvailability;
        updateRegisterButtonState();
        return emailAvailable;
    }

    lastEmailCheckedValue = email;
    lastEmailAvailability = null;
    latestEmailCheck += 1;
    const requestId = latestEmailCheck;
    setHelperText(emailFeedback, 'Checking availability...', 'info');

    try {
        const available = await checkAvailability('email', email);
        if (requestId !== latestEmailCheck) {
            return emailAvailable;
        }

        emailAvailable = available;
        lastEmailAvailability = available;
        if (available) {
            emailFeedback.textContent = '';
        } else {
            setHelperText(emailFeedback, 'This email is already registered. Please log in or use another email.', 'error');
        }
    } catch (error) {
        if (requestId !== latestEmailCheck) {
            return emailAvailable;
        }
        emailAvailable = false;
        lastEmailAvailability = null;
        lastEmailCheckedValue = '';
        setHelperText(emailFeedback, error.message || 'Unable to check email availability.', 'error');
    }

    updateRegisterButtonState();
    return emailAvailable;
};

const handleStudentIdAvailability = async () => {
    validateStudentId();
    if (!studentIdValid) {
        studentIdAvailable = false;
        lastStudentIdCheckedValue = '';
        lastStudentIdAvailability = null;
        updateRegisterButtonState();
        return false;
    }

    const studentId = studentIdInput.value.trim();
    if (studentId === lastStudentIdCheckedValue && lastStudentIdAvailability !== null) {
        studentIdAvailable = lastStudentIdAvailability;
        updateRegisterButtonState();
        return studentIdAvailable;
    }

    lastStudentIdCheckedValue = studentId;
    lastStudentIdAvailability = null;
    latestStudentIdCheck += 1;
    const requestId = latestStudentIdCheck;
    setHelperText(studentIdFeedback, 'Checking availability...', 'info');

    try {
        const available = await checkAvailability('student_id', studentId);
        if (requestId !== latestStudentIdCheck) {
            return studentIdAvailable;
        }

        studentIdAvailable = available;
        lastStudentIdAvailability = available;
        if (available) {
            studentIdFeedback.textContent = '';
        } else {
            setHelperText(studentIdFeedback, 'This student ID is already registered.', 'error');
        }
    } catch (error) {
        if (requestId !== latestStudentIdCheck) {
            return studentIdAvailable;
        }
        studentIdAvailable = false;
        lastStudentIdAvailability = null;
        lastStudentIdCheckedValue = '';
        setHelperText(studentIdFeedback, error.message || 'Unable to check student ID right now.', 'error');
    }

    updateRegisterButtonState();
    return studentIdAvailable;
};

const updateRegisterButtonState = () => {
    registerBtn.disabled = !(otpVerified && emailAvailable && studentIdValid && studentIdAvailable && passwordValid && passwordsMatch);
};

const resetOtpState = () => {
    otpVerified = false;
    otpInput.value = '';
    otpInput.disabled = false;
    verifyOtpBtn.disabled = false;
    verifyOtpBtn.textContent = 'Verify OTP';
    verifyOtpBtn.classList.remove('success');
    otpWrapper.hidden = true;
    setHelperText(otpStatus, '');
    setHelperText(otpFeedback, '');
    updateRegisterButtonState();
};

const startResendCooldown = () => {

    if(!document.getElementById('request-otp')) return;

    let remaining = 120;
    requestOtpBtn.disabled = true;
    requestOtpBtn.textContent = `Resend in ${remaining}s`;

    resendTimer = setInterval(() => {
        remaining -= 1;
        if (remaining <= 0) {
            clearInterval(resendTimer);
            resendTimer = null;
            requestOtpBtn.disabled = false;
            requestOtpBtn.textContent = 'Get OTP';
        } else {
            requestOtpBtn.textContent = `Resend in ${remaining}s`;
        }
    }, 1000);
};

const startVerifyCooldown = () => {
    if (!document.getElementById('verify-otp')) return;

    let remaining = 5;
    verifyOtpBtn.disabled = true;
    verifyOtpBtn.textContent = `Retry in ${remaining}s`;

    const verifyTimer = setInterval(() => {
        remaining -= 1;
        if (remaining <= 0) {
            clearInterval(verifyTimer);
            verifyOtpBtn.disabled = false;
            verifyOtpBtn.textContent = 'Verify OTP';
        } else {
            verifyOtpBtn.textContent = `Retry in ${remaining}s`;
        }
    }, 1000);
};

const validateEmail = () => {
    const email = emailInput.value.trim();
    if (!email) {
        setHelperText(emailFeedback, 'Email is required.', 'error');
        return false;
    }
    if (!EMAIL_DOMAIN_REGEX.test(email)) {
        setHelperText(emailFeedback, 'Use your institutional email (example@student.nstu.edu.bd).', 'error');
        return false;
    }
    //setHelperText(emailFeedback, 'Valid institutional email detected.', 'success');
    return true;
};

const validatePasswordStrength = () => {
    const value = passwordInput.value.trim();
    if (!value) {
        setHelperText(passwordFeedback, 'Password is required.', 'error');
        passwordValid = false;
        return;
    }
    if (!PASSWORD_REGEX.test(value)) {
        setHelperText(passwordFeedback, 'Use at least 8 characters and at least one number.', 'error');
        passwordValid = false;
    } else {
        passwordFeedback.textContent = '';
        passwordValid = true;
    }
};

const validateStudentId = () => {
    const rawValue = studentIdInput.value.trim();
    if (!rawValue) {
        setHelperText(studentIdFeedback, 'Student ID is required.', 'error');
        studentIdValid = false;
        return;
    }

    const value = rawValue.toUpperCase();
    if (value !== rawValue) {
        studentIdInput.value = value;
    }

    if (!STUDENT_ID_REGEX.test(value)) {
        setHelperText(
            studentIdFeedback,
            'Enter valid student id (e.g., ASH2101000M).',
            'error'
        );
        studentIdValid = false;
    } else {
        studentIdFeedback.textContent = '';
        studentIdValid = true;
    }
};

const validatePasswordMatch = () => {
    const password = passwordInput.value.trim();
    const confirm = confirmPasswordInput.value.trim();

    if (!confirm) {
        setHelperText(confirmPasswordFeedback, 'Please confirm your password.', 'error');
        passwordsMatch = false;
        return;
    }

    if (password !== confirm) {
        setHelperText(confirmPasswordFeedback, "Passwords don't match.", 'error');
        passwordsMatch = false;
    } else {
        setHelperText(confirmPasswordFeedback, 'Passwords match ✔', 'success');
        passwordsMatch = true;
    }
};

// Event listeners
emailInput.addEventListener('input', () => {
    if (resendTimer) {
        clearInterval(resendTimer);
        resendTimer = null;
        requestOtpBtn.textContent = 'Get OTP';
        requestOtpBtn.disabled = false;
    }
    setHelperText(emailFeedback, '');
    resetOtpState();
    validateEmail();
    emailAvailable = false;
    lastEmailCheckedValue = '';
    lastEmailAvailability = null;
    updateRegisterButtonState();
});

emailInput.addEventListener('blur', () => {
    if (emailInput.value.trim()) {
        handleEmailAvailability();
    }
});

requestOtpBtn.addEventListener('click', async () => {
    const email = emailInput.value.trim();
    if (!validateEmail()) {
        return;
    }

    const available = await handleEmailAvailability();
    if (!available) {
        return;
    }

    setHelperText(otpFeedback, '');
    setHelperText(otpStatus, 'Sending OTP...', 'info');
    otpWrapper.hidden = false;
    otpInput.focus();

    try {
        const response = await fetch('/send_otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin',
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Failed to send OTP');
        }

        setHelperText(otpStatus, 'OTP sent to your email. Please check your inbox.', 'info');
        startResendCooldown();
    } catch (error) {
        setHelperText(otpStatus, error.message || 'Unable to send OTP. Please try again later.', 'error');
    }
});

verifyOtpBtn.addEventListener('click', async () => {
    const email = emailInput.value.trim();
    const otp = otpInput.value.trim();

    if (!validateEmail()) {
        return;
    }

    if (otp.length !== 6) {
        setHelperText(otpFeedback, 'OTP must be 6 digits.', 'error');
        return;
    }

    verifyOtpBtn.disabled = true;
    //setHelperText(otpFeedback, 'Verifying...', 'info');

    try {
        const response = await fetch('/verify_otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin',
            body: JSON.stringify({ email, otp })
        });

        const data = await response.json();

        if (!response.ok) {
            startVerifyCooldown();
            throw new Error(data.message || 'OTP verification failed');
        }

        otpVerified = true;
        otpInput.disabled = true;
        verifyOtpBtn.textContent = 'Verified';
        verifyOtpBtn.classList.add('success');
        verifyOtpBtn.disabled = true;
        //setHelperText(otpFeedback, 'OTP verified successfully.', 'success');
        
        setHelperText(emailFeedback, 'Email verified successfully.', 'success');
        updateRegisterButtonState();

        const div_otp_controls = document.querySelector(".otp-controls");
        if (div_otp_controls) {
            div_otp_controls.remove();
        }

        otpFeedback.textContent = '';
    } catch (error) {
        setHelperText(otpFeedback, error.message || 'Invalid OTP. Please try again.', 'error');
    }
});

passwordInput.addEventListener('input', () => {
    validatePasswordStrength();
    validatePasswordMatch();
    updateRegisterButtonState();
});

confirmPasswordInput.addEventListener('input', () => {
    validatePasswordMatch();
    updateRegisterButtonState();
});

studentIdInput.addEventListener('input', () => {
    validateStudentId();
    studentIdAvailable = false;
    lastStudentIdCheckedValue = '';
    lastStudentIdAvailability = null;
    updateRegisterButtonState();
});

studentIdInput.addEventListener('blur', () => {
    if (studentIdInput.value.trim()) {
        handleStudentIdAvailability();
    }
});

form.addEventListener('submit', (event) => {
    validateStudentId();
    validatePasswordStrength();
    validatePasswordMatch();
    updateRegisterButtonState();

    if (registerBtn.disabled) {
        event.preventDefault();
        if (!otpVerified) {
            setHelperText(otpFeedback, 'Please verify the OTP before registering.', 'error');
        }
        if (!studentIdValid) {
            setHelperText(studentIdFeedback, 'Please provide a valid Student ID.', 'error');
        }
    }
});

// Initial state for controls
updateRegisterButtonState();

// Password visibility toggle
const togglePassword = document.getElementById('togglePassword');

if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function(e) {
        // Toggle password visibility
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // Toggle eye icon
        this.querySelector('i').className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
    });
}
