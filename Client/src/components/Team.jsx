// import React from 'react';
import Selasi from "../assets/Selasi.jpeg";
import Paul from "../assets/Paul.jpeg";
import Oliver from "../assets/Oliver.jpeg";
// import Duaa from "../assets/Duaa.jpeg";

const Team = () => {
  const teamMembers = [
    {
      name: "Duaa Obeid",
      role: "Backend Engineer",
      // image: Duaa,
      description:
        "Duaa Obeid is a skilled backend engineer, proficient in building scalable systems, optimizing performance, and ensuring robust server-side functionality. ",
    },
    {
      name: "Oliver Maketso",
      role: "Backend Devloper",
      image: Oliver,
      description:
        "Oliver Maketso is a backend developer, specializing in APIs, database management, and efficient server-side architectures.",
    },
    {
      name: "Paul Levites",
      role: "Frontend Devloper",
      image: Paul,
      description:
        "Paul Levites is a skilled frontend developer, experienced in building intuitive, visually appealing, and high-performing user interfaces with a focus on accessibility and responsiveness.",
    },
    {
      name: "Selasi Mensah",
      role: "Frontend Developer",
      image: Selasi,
      description:
        "Selasi Mensah is a creative frontend developer skilled in creating responsive designs, interactive user interfaces, and seamless experiences using modern frameworks like React and Vue.js.",
    },
  ];

  return (
    <div id="meet" className="p-8 bg-gray-100">
      <h2 className="text-3xl font-bold text-center mb-6">Meet Our Team</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {teamMembers.map((member, index) => (
          <div
            key={index}
            className="bg-white shadow-lg rounded-2xl p-6 flex flex-col items-center text-center"
          >
            <img
              src={member.image}
              alt={member.name}
              className="w-30 h-24 rounded-full mb-2"
            />
            <h3 className="text-xl font-semibold">{member.name}</h3>
            <p className="text-gray-500 mb-2">{member.role}</p>
            <p className="text-gray-600 text-sm">{member.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Team;
