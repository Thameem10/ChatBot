import { CheckCircle, Send } from "lucide-react";
import { useState } from "react";
import { createWithAuth } from "../services/apiClient";

interface FormData {
  fullname: string;
  email: string;
  phoneno: string;
  subject: string;
  message: string;
  inquirytype: string;
}

interface FormErrors {
  fullname?: string;
  email?: string;
  phoneno?: string;
  subject?: string;
  message?: string;
}

export default function ContactForm() {
  const [formData, setFormData] = useState<FormData>({
    fullname: "",
    email: "",
    phoneno: "",
    subject: "",
    message: "",
    inquirytype: "general"
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const API_URL = import.meta.env.VITE_API_URL;

  // Live validation per field
  const validateField = (name: string, value: string): string => {
    let error = "";
    switch (name) {
      case "fullname":
        if (!value.trim()) error = "Full name is required";
        else if (value.trim().length < 3)
          error = "Full name must be at least 3 characters";
        else if (!/^[A-Za-z\s]+$/.test(value))
          error = "Full name can only contain letters and spaces";
        break;
      case "email":
        if (!value.trim()) error = "Email is required";
        else if (!/\S+@\S+\.\S+/.test(value))
          error = "Please enter a valid email address";
        break;
      case "phoneno":
        if (value.trim() && !/^\d{10}$/.test(value))
          error = "Phone number must be 10 digits";
        break;
      case "subject":
        if (!value.trim()) error = "Subject is required";
        break;
      case "message":
        if (!value.trim()) error = "Message is required";
        break;
      default:
        break;
    }
    setErrors((prev) => ({ ...prev, [name]: error }));
    return error;
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};
    (Object.keys(formData) as Array<keyof FormErrors>).forEach((key) => {
      const error = validateField(key, formData[key] as string);
      if (error) newErrors[key] = error;
    });
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    validateField(name, value); // live validation
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return; // stop if validation fails

    setIsSubmitting(true);

    try {
      const apiUrl = `${API_URL}/contact/create-contact`;
      const result = await createWithAuth<any>(apiUrl, formData);
      console.log("Form submission result:", result);
      if (result) {
        setIsSubmitted(true);
        setFormData({
          fullname: "",
          email: "",
          phoneno: "",
          subject: "",
          message: "",
          inquirytype: "general"
        });
      } else {
        alert("Failed to submit form: " + result);
      }
    } catch (err) {
      console.error(err);
      alert("Error submitting form");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
          <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Message Sent Successfully!
          </h2>
          <p className="text-gray-600 mb-6">
            Thank you for contacting us. Our team will get back to you within 24
            hours.
          </p>
          <button
            onClick={() => setIsSubmitted(false)}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Send Another Message
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="w-fit flex flex-col justify-center items-center mx-auto mt-10">
      <h2 className="text-3xl font-bold text-gray-900 mb-8">
        Send us a Message
      </h2>
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Full Name */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Full Name *
          </label>
          <input
            type="text"
            name="fullname"
            value={formData.fullname}
            onChange={handleInputChange}
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 ${
              errors.fullname ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="Your full name"
          />
          {errors.fullname && (
            <p className="text-red-600 text-sm mt-1">{errors.fullname}</p>
          )}
        </div>

        {/* Email */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Email Address *
          </label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 ${
              errors.email ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="your.email@example.com"
          />
          {errors.email && (
            <p className="text-red-600 text-sm mt-1">{errors.email}</p>
          )}
        </div>

        {/* Phone Number */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Phone Number
          </label>
          <input
            type="tel"
            name="phoneno"
            value={formData.phoneno}
            onChange={handleInputChange}
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 ${
              errors.phoneno ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="10 digit number"
          />
          {errors.phoneno && (
            <p className="text-red-600 text-sm mt-1">{errors.phoneno}</p>
          )}
        </div>

        {/* Subject */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Subject *
          </label>
          <input
            type="text"
            name="subject"
            value={formData.subject}
            onChange={handleInputChange}
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 ${
              errors.subject ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="Subject"
          />
          {errors.subject && (
            <p className="text-red-600 text-sm mt-1">{errors.subject}</p>
          )}
        </div>

        {/* Message */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Message *
          </label>
          <textarea
            name="message"
            value={formData.message}
            onChange={handleInputChange}
            rows={6}
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 ${
              errors.message ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="Your message"
          />
          {errors.message && (
            <p className="text-red-600 text-sm mt-1">{errors.message}</p>
          )}
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-gradient-primary text-white px-6 py-4 rounded-lg font-semibold hover:bg-gradient-primary-hover transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {isSubmitting ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Sending...</span>
            </>
          ) : (
            <>
              <Send className="h-5 w-5" />
              <span>Send Message</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
