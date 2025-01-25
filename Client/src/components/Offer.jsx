import Card from "./Card";

const Offer = () => {
  return (
    <div id="offer" className="bg-[#E6E5D2] my-5 py-[30px] md:py-[50px] px-[30px] ">
      <div className="text-center flex flex-col gap-[20px]">
        <p className="text-[32px] md:text-[40px] lg:text-[48px] font-medium md:font-normal leading-[54px] md:leading-[80px]">
          What We Offer
        </p>
      </div>

      <div className="flex gap-[20px] lg:gap-[50px] mt-[50px] items-center flex-wrap justify-center flex-col md:flex-row">
        <Card
          src={"Artisan + Client"}
          //   title={"Artisan + Client"}
          content={
            "Hirafic is a dynamic platform dedicated to bridging the gap between skilled artisans with low-paying expertise and clients seeking quality, affordable craftsmanship. By offering a digital space for artisans to showcase their talents, Hirafic empowers individuals in underserved communities to gain visibility, expand their client base, and secure sustainable livelihoods."
          }
        />
        <Card
          src={"MarketPlace"}
          //   title={"New Patient Onboarding Part 1"}
          content={
            "The platform operates as a marketplace where artisans can create detailed profiles to highlight their skills, portfolios, and services. Clients can easily browse profiles, post project requests, or collaborate on custom services. Hirafic ensures transparency, fair pricing, and secure payments, enabling artisans to earn a fair income for their work."
          }
        />
        <Card
          src={"Pathway to financial independence"}
          //   title={"Advanced Diagnostic and Laboratory Testing"}
          content={
            "For artisans, Hirafic is more than a marketplace—it’s a pathway to financial independence and recognition. By connecting them with local and global clients, the platform helps them transcend geographical and economic barriers. Clients, on the other hand, gain access to unique, high-quality, and affordable craftsmanship while supporting local economies."
          }
        />
        <Card
          src={"Community development"}
          //   title={"New Patient Onboarding Part 2"}
          content={
            "Hirafic is committed to social impact, reinvesting part of its earnings into community development initiatives like training programs and artisan fairs. Looking ahead, the platform aims to integrate advanced technologies to further enhance the user experience. Hirafic stands as a beacon of hope for skilled artisans, proving that even the most modest crafts can create lasting value and transform lives."
          }
        />
        {/* <Card
          src={"STEP 5"}
          title={"Start Your Journey"}
          content={
            "Clinical support session with one of our nurses or health coaches to review recommendations and program onboarding with our Patient Journey Director"
          }
        /> */}
      </div>
    </div>
  );
};

export default Offer;
