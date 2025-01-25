const Card = ({ src, title, content }) => {
    return (
      <div className="flex flex-col gap-[18px]  px-[30px] py-[98px] border-b-[0px]  rounded-[20px] border-t-[1px] border-x-[1px] w-fit md:w-[43%] lg:w-[33.3%] group hover:bg-[#747762]">
        {/* <img src={src} alt="" /> */}
        {/* <i className={`fa-solid ${src} text-[48px] group-hover:text-white`}></i> */}
        <p className="text-[20px] text-[#A9AE97] font-semibold leading-[24px] group-hover:text-white">
          {src}
        </p>
        <p className="text-[20px] font-semibold leading-[24px] group-hover:text-white">
          {title}
        </p>
        <p className="text-[14px] font-bold leading-[30px] font-inter group-hover:text-white ">
          {content}
        </p>
      </div>
    );
  };
  
  export default Card;
  