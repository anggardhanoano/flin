import * as Yup from "yup";

export const inquirySchema = Yup.object({
  name: Yup.string()
    .required("Name is required")
    .min(2, "Name must be at least 2 characters"),
  email: Yup.string()
    .email("Invalid email address")
    .required("Email is required"),
  phone_number: Yup.string()
    .matches(
      /^(\+?[1-9]\d{1,14}|[0-9]{10,15})$/,
      "Phone number must be a valid international phone number or a local number with 10 to 15 digits"
    )
    .min(10, "Phone number must be at least 10 digits")
    .max(15, "Phone number must be at most 15 digits")
    .required("Phone number is required"),
  loan_type: Yup.string().required("Loan type is required"),
});
