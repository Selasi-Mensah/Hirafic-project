// import React from "react";
import headerimg from "./../assets/Hero2.webp";
import { Link } from "react-router-dom";
const Header = () => {
  return (
    <div className="flex md:pl-[30px] /h-[100vh] pt-[70px] md:pt-[80px] flex-col-reverse md:flex-row">
      <div className="basis-1/2 pt-[40px] m-1 flex flex-col gap-[20px] lg:gap-[30px] pl-[30px] md:pl-[0px]">
        <p className="text-[22px] md:text-[48px] lg:text-[30px] font-bold font-poppins leading-[30px] md:leading-[60px] lg:leading-[40px] ">
          Hirafic: Empowering Artisans, Connecting Communities
        </p>
        <p className="text-[13px] lg:text-[15px] leading-[20px] lg:leading-[32px] font-inter font-bold">
          Hirafic is a dynamic platform dedicated to bridging the gap between
          skilled artisans with low-paying expertise and clients seeking
          quality, affordable craftsmanship. By offering a digital space for
          artisans to showcase their talents, Hirafic empowers individuals in
          underserved communities to gain visibility, expand their client base,
          and secure sustainable livelihoods. <br />
          <br />
          The platform operates as a marketplace where artisans can create
          detailed profiles to highlight their skills, portfolios, and services.
          Clients can easily browse profiles, post project requests, or
          collaborate on custom services. Hirafic ensures transparency, fair
          pricing, and secure payments, enabling artisans to earn a fair income
          for their work. <br />
          <br />
          {/* For artisans, Hirafic is more than a marketplace—it’s a pathway to
          financial independence and recognition. By connecting them with local
          and global clients, the platform helps them transcend geographical and
          economic barriers. Clients, on the other hand, gain access to unique,
          high-quality, and affordable craftsmanship while supporting local
          economies. <br />
          <br />
          Hirafic is committed to social impact, reinvesting part of its
          earnings into community development initiatives like training programs
          and artisan fairs. Looking ahead, the platform aims to integrate
          advanced technologies to further enhance the user experience. Hirafic
          stands as a beacon of hope for skilled artisans, proving that even the
          most modest crafts can create lasting value and transform lives. */}
        </p>

        <Link
          to="/register"
          className="text-white bg-[#161622] font-[500] text-[20px] lg:text-[18px] leading-[28px] lg:leading-[32px] py-[2px] px-[18px] rounded-[30px] self-start"
        >
          Join Hirafic
        </Link>
      </div>

      <div className="basis-1/2 w-full h-[90vh]">
        <img
          src={headerimg}
          alt=""
          className="w-full h-full object-cover rounded-bl-[80px]"
        />
      </div>
    </div>
  );
};

export default Header;
