// import React from "react";
import { useForm, ValidationError } from "@formspree/react";
import { useNavigate } from "react-router-dom";

const Contact = () => {
  const navigate = useNavigate();
  const [state, handleSubmit] = useForm("mjkgvzpw");
  if (state.succeeded) {
    setTimeout(() => {
      navigate("/");
    }, 4000);
    return (
      <div className="flex flex-col bg-[#E6E5D2]  items-center justify-center w-full min-h-screen">
        {/* <ion-icon name="reload"></ion-icon> */}
        <p className="pt-2 text-md text-teal-700 ">
          Thanks For Reaching out. We will get back to you
        </p>
      </div>
    );
  }
  return (
    <div className="antialiased bg-[#202020] ">
      <div className="flex w-full min-h-screen justify-center items-center">
        <div className="flex flex-col  md:flex-row md:space-x-6 space-y-6 md:space-y-0 bg-[#E6E5D2] w-full max-w-4xl p-8 sm:p-10 rounded-xl shadow-lg text-[#090720]">
          <div className="flex flex-col space-y-8 justify-around">
            <div>
              <h1 className="font-bold text-2xl tracking-wide">
                Still have questions?
              </h1>
              <p className="pt-2 text-sm">
                Use this quick contact form to send us a message and our team
                will get back to you as soon as we can.
              </p>
            </div>
            <div className="flex flex-col space-y-6">
              {/* <div className="inline-flex space-x-2 items-center">
                <ion-icon
                  name="call"
                  //   className="text-teal-300 text-xl"
                ></ion-icon>
                <span>+234-810-000-0001</span>
              </div> */}
              {/* <div className="inline-flex space-x-2 items-center">
                <ion-icon name="mail"></ion-icon>
                <span>Paullevites84@gmail.com</span>
              </div> */}
              {/* <div className="inline-flex space-x-2 items-center">
                <ion-icon name="location"></ion-icon>
                <span>372 Danbury Rd, Suite 220, Wilton, CT 06897.</span>
              </div> */}
            </div>
          </div>
          <div>
            <div className="bg-white rounded-xl shadow-lg p-8 md:w-80">
              <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
                <div>
                  <label htmlFor="">Full Name</label>
                  <input
                    type="text"
                    className="ring-1 ring-gray w-full mt-2 rounded-md px-4 py-2 outline-none focus:ring-2 focus:ring-teal-300"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="">Email Address</label>
                  <input
                    type="email"
                    className="ring-1 ring-gray w-full mt-2 rounded-md px-4 py-2 outline-none focus:ring-2 focus:ring-teal-300"
                    required
                    name="email"
                    id="email"
                  />
                  <ValidationError
                    prefix="Email"
                    field="email"
                    errors={state.errors}
                  />
                </div>
                <div>
                  <label htmlFor="">Your Question</label>
                  <textarea
                    rows="6"
                    className="ring-1 resize-none ring-gray w-full mt-2 rounded-md px-4 py-2 outline-none focus:ring-2 focus:ring-teal-300"
                    name="message"
                    id="message"
                  ></textarea>
                  <ValidationError
                    prefix="Message"
                    field="message"
                    errors={state.errors}
                  />
                </div>
                <button
                  disabled={state.submitting}
                  className="inline-block self-start bg-[#E6E5D2] font-bold rounded-lg px-6 py-2 uppercase text-sm"
                >
                  Submit
                </button>
                <button
                  type="button"
                  onClick={() => navigate("/about")}
                  className="inline-block self-start bg-red-500 text-white font-bold rounded-lg px-6 py-2 uppercase text-sm"
                >
                  Close
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;
