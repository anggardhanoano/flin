import { useFormik } from "formik";
import { inquirySchema } from "./validation";

function App() {
  const formik = useFormik({
    initialValues: {
      name: "",
      email: "",
      phone_number: "",
      loan_type: "personal",
    },
    validationSchema: inquirySchema,
    onSubmit: async (values, { resetForm }) => {
      console.log("Form submitted:", values);
      //  use fetch api to post the data to the server
      const response = await fetch("http://localhost:8000/leads/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values),
      });

      if (!response.ok) {
        const errorResponse = await response.json();
        const error = errorResponse.error;
        // Handle error response
        console.error("Error submitting form:", error);
        alert("Error submitting form. Please try again.");
        return;
      }
      const data = await response.json();
      console.log("Response from server:", data);
      // Handle success response
      alert("Form submitted successfully!");
      resetForm();
    },
  });

  return (
    <div className="w-screen h-screen flex flex-col justify-center items-center gap-4">
      <h1 className="text-xl font-bold">Create Inquiry</h1>
      <div className="flex flex-col w-1/3 min-w-[200px]">
        <div className="flex flex-col">
          <label htmlFor="name" className="text-sm font-bold">
            Name
          </label>
          <input
            id="name"
            name="name"
            type="text"
            placeholder="Enter your name"
            className="border-2 border-gray-300 rounded-md p-2 mb-1"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.name}
          />
          {formik.touched.name && formik.errors.name ? (
            <div className="text-red-500 text-sm mb-2">
              {formik.errors.name}
            </div>
          ) : (
            <div className="mb-3"></div>
          )}
        </div>

        <div className="flex flex-col">
          <label htmlFor="email" className="text-sm font-bold">
            Email
          </label>
          <input
            id="email"
            name="email"
            type="email"
            placeholder="Enter your email"
            className="border-2 border-gray-300 rounded-md p-2 mb-1"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.email}
          />
          {formik.touched.email && formik.errors.email ? (
            <div className="text-red-500 text-sm mb-2">
              {formik.errors.email}
            </div>
          ) : (
            <div className="mb-3"></div>
          )}
        </div>

        <div className="flex flex-col">
          <label htmlFor="phone_number" className="text-sm font-bold">
            Phone number
          </label>
          <input
            id="phone_number"
            name="phone_number"
            type="text"
            placeholder="Enter your phone number"
            className="border-2 border-gray-300 rounded-md p-2 mb-1"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.phone_number}
          />
          {formik.touched.phone_number && formik.errors.phone_number ? (
            <div className="text-red-500 text-sm mb-2">
              {formik.errors.phone_number}
            </div>
          ) : (
            <div className="mb-3"></div>
          )}
        </div>

        <div className="flex flex-col">
          <label htmlFor="loan_type" className="text-sm font-bold">
            Loan Type
          </label>
          <select
            id="loan_type"
            name="loan_type"
            className="border-2 border-gray-300 rounded-md p-2 mb-4"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.loan_type}
          >
            <option value="personal">Personal Loan</option>
            <option value="kpr">KPR</option>
            <option value="kpa">KPA</option>
          </select>
        </div>

        <button
          type="button"
          onClick={() => formik.handleSubmit()}
          className="bg-blue-500 text-white py-2 px-4 rounded-md w-full hover:bg-blue-600"
        >
          Submit Inquiry
        </button>
      </div>
    </div>
  );
}

export default App;
