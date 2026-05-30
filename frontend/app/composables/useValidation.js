/**
 * Description placeholder
 *
 * @returns {{ requireEmail: (email: any, label?: string) => boolean; requirePassword: (password: any, label?: string) => boolean; validatePasswordLength: (password: any) => boolean; validatePasswordMatch: (password: any, confirmPassword: any) => boolean; }} 
 */
export const useValidation = () => {
    const { showPopup } = usePopup();

    function requireEmail(email, label = "email") {
        if (!email.trim()) {
            showPopup(`Please enter your ${label} first.`, "error");
            return false;
        }

        return true;
    }

    function requirePassword(password, label = "password") {
        if (!password) {
            showPopup(`Please enter your ${label} first.`, "error");
            return false;
        }

        return true;
    }

    function validatePasswordLength(password) {
        if (password.length < 8) {
            showPopup("Password must contain at least 8 characters.", "error");
            return false;
        }

        return true;
    }

    function validatePasswordMatch(password, confirmPassword) {
        if (password !== confirmPassword) {
            showPopup("Passwords do not match.", "error");
            return false;
        }

        return true;
    }

    return {
        requireEmail,
        requirePassword,
        validatePasswordLength,
        validatePasswordMatch,
    };
};
