import  { useState, useEffect } from "react";
import axios from "axios";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import ProfileSection from "@/components/ProfileSection";
import LoadingState from "@/components/LoadingState";
import ErrorState from "@/components/ErrorState";
import BookingCard from "@/components/BookingCard";
import CloseIcon from "@mui/icons-material/Close";
import MenuOpenIcon from "@mui/icons-material/MenuOpen";
import Hirafic from "@/assets/Hirafic.jpg";

const Artisan = () => {
  const [bookings, setBookings] = useState([]);
  const [bookingsPagination, setBookingPage] = useState({
    bookings: [],
    total_pages: 0,
    current_page: 0,
  });
  const [profile, setProfile] = useState({
    username: '',
    email: '',
    phone_number: '',
    location: '',
    specialization: '',
    skills: '',
    salary_per_hour: '',
    image_file: ''
  });
  const [loading, setLoading] = useState({
    bookings: true,
    artisans: true,
    profile: true,
  });
  const [error, setError] = useState({
    bookings: null,
    artisans: null,
    profile: null,
  });

  const [file, setFile] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const token = sessionStorage.getItem("access_token");
  const name = sessionStorage.getItem("username");
  const [page, setPage] = useState(1);
  const per_page = 3;
  const [activeTab, setActiveTab] = useState('');

  const fetchData = async (
    endpoint,
    setter,
    loadingKey,
    errorKey,
    options = {}
  ) => {
    try {
      setLoading((prev) => ({ ...prev, [loadingKey]: true }));
      setError((prev) => ({ ...prev, [errorKey]: null }));

      // Build query parameters if provided
      const queryParams = options.params
        ? "?" + new URLSearchParams(options.params).toString()
        : "";

      const response = await fetch(
        `http://127.0.0.1:5000${endpoint}${queryParams}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (response.status === 401) {
        if (sessionStorage.getItem('access_token')) {
          sessionStorage.removeItem('access_token');
          sessionStorage.clear();
          window.location.href = '/login';
          alert('Session expired. Please login again');
          return;
        }
        else {
          return < Redirect to='/login' />;
        }
      }
      else if (response.status !== 200) {
        alert('An error occurred');
      }
      const data = await response.json();
      setter(data);
    } catch (err) {
      setError((prev) => ({
        ...prev,
        [errorKey]: err.message || "An error occurred",
      }));
    } finally {
      setLoading((prev) => ({ ...prev, [loadingKey]: false }));
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    console.log(e.target.files[0]);
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  useEffect(() => {
    // Fetch profile details for client
    fetchData('/artisan', setProfile, 'profile', 'profile');
    
    // Fetch paginated bookings for client
    fetchData('/bookings', (response) => {
      // Extract and set pagination details
      setBookingPage((prev) => ({
        ...prev,
        bookings: response.bookings,
        current_page: response.current_page,
        total_pages: response.total_pages,
      }));
      setBookings(response.bookings);
    }, 'bookings', 'bookings', {
      params: {activeTab, page: page, per_page: per_page},
    });

  }, [activeTab, page, per_page]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile((prevProfile) => ({
      ...prevProfile,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading({ profile: true });
    setError({ profile: null });

    const formData = new FormData();
    formData.append('username', profile.username);
    formData.append('email', profile.email);
    formData.append('phone_number', profile.phone_number);
    formData.append('location', profile.location);
    formData.append('skills', profile.skills);
    formData.append('specialization', profile.specialization);
    formData.append('salary_per_hour', profile.salary_per_hour);
    if (file) {
      formData.append("picture", file);
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/artisan', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      if (response.status === 401) {
        if (sessionStorage.getItem('access_token')) {
          sessionStorage.removeItem('access_token');
          sessionStorage.clear();
          window.location.href = '/login';
          alert('Session expired. Please login again');
          return;
        }
        else {
          return;
        }
      }
      setProfile(response.data);
      alert("Profile updated successfully");
    } catch (err) {
      setError({ profile: err.message });
    } finally {
      setLoading({ profile: false });
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem('access_token');
    sessionStorage.clear();
    window.location.href = '/login';
  };

  const handleAbout = () => {
    window.location.href = "/About";
  };

  const handlePageChange = (newPage) => setPage(newPage);

  return (
    <div className="min-h-screen bg-[#E6E5D2] text-gray-100 py-8 flex items-center justify-center">
       <div className="max-w-7xl mx-auto px-4">
        {/* Sidebar */}
        {isSidebarOpen && (
          <aside className="bg-gray-900 w-80 min-h-screen px-6 py-20 transition-all duration-300 fixed top-0 left-0 z-20">
            <h2 className="text-l text-center font-bold text-white mb-8">
              Navigation
            </h2>
            <ul className="space-y-4">
              <li>
                <button
                  onClick={handleAbout}
                  className="w-full items-center gap-4 bg-gray-800 hover:bg-gray-700 text-white py-1 px-1 rounded-md transition-all duration-300"
                >
                  <span className="material-icons">About</span>
                </button>
              </li>
              <li>
                <button
                  onClick={handleLogout}
                  className="w-full items-center gap-4 bg-red-600 hover:bg-red-700 text-white py-1 px-1 rounded-md transition-all duration-300"
                >
                  <span className="material-icons">Logout</span>
                </button>
              </li>
            </ul>
          </aside>
        )}

        {/* Header */}
        <main className="items-center justify-center px-8 py-8">
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="bg-gray-800 text-white hover:bg-gray-700 px-4 py-2 rounded-md absolute top-4 left-4 z-10"
          >
            {/* {isSidebarOpen ? 'Close Sidebar' : 'Open Sidebar'} */}
          </button>
          {/* Open Sidebar Button */}
          <button
            onClick={() => setIsSidebarOpen(true)}
            className="bg-gray-800 text-white hover:bg-gray-700 p-3 rounded-md absolute top-4 left-2 z-10"
          >
            <MenuOpenIcon />
          </button>

          {/* Close Sidebar Button */}
          {isSidebarOpen && (
            <button
              onClick={() => setIsSidebarOpen(false)}
              className="bg-gray-800 text-white hover:bg-gray-700 p-3 rounded-md absolute top-4 left-2 z-50"
            >
              <CloseIcon />
            </button>
          )}
          
          {activeTab === '' && (
            <div className="text-center flex flex-col items-center">
              {/* Welcome Message */}
              <h2 className="text-3xl font-bold mb-4 text-gray-200">
                Welcome, {sessionStorage.getItem("username")}
              </h2>
              <p className="text-gray-400 text-lg mb-4">
                Use the navigation menu or select a tab to explore.
              </p>
            </div>
          )}
          {activeTab === 'profile' && (
           <div className="text-center flex flex-col items-center ">
              <h2 className="text-3xl font-bold mb-4 text-gray-900">My Profile</h2>
              <p className="text-gray-700 text-lg mb-4">
                Manage your account details and preferences here.
              </p>
            </div>
          )}
          {activeTab === 'bookings' && (
            <div className="text-center flex flex-col items-center ">
              <h2 className="text-3xl font-bold mb-4 text-gray-900">Bookings Details</h2>
              <p className="text-gray-700 text-lg mb-4">
                View and manage your bookings here.
              </p>
            </div>
          )}

          <Tabs defaultValue="bookings" className="mx-auto" onValueChange={handleTabChange}>
            <div className='text-center'>
              <TabsList className="flex bg-gray-900 text-gray-100 w-[350px] mx-auto gap-6 mb-4">
                <TabsTrigger
                  value="profile"
                  className=" w-[225px] data-[state=active]:bg-gray-800"
                >
                  Profile
                </TabsTrigger>
                <TabsTrigger
                  value="bookings"
                  className=" w-[225px] data-[state=active]:bg-gray-800"
                >
                  Bookings
                </TabsTrigger>
              </TabsList>
            </div>

            <TabsContent value="profile">
              <ProfileSection
                profile={profile}
                loading={loading}
                error={error}
                handleSubmit={handleSubmit}
                handleChange={handleChange}
                handleFileChange={handleFileChange}
                editable={true}
              />
            </TabsContent>

            <TabsContent value="bookings">
              <div className="bg-gray-900 text-gray-100 p-6 rounded-lg shadow-md max-w-md mx-auto grid gap-2">
                {loading.bookings ? (
                  <LoadingState />
                ) : error.bookings ? (
                  <ErrorState message={error.bookings} />
                ) : bookings.length > 0 ? (
                  bookings.map((booking) => (
                    <BookingCard key={booking.id} booking={booking} />
                  ))
                ) : (
                  <p className="text-center text-gray-400">
                    No bookings found.
                  </p>
                )}
              </div>
              <div className="flex items-center justify-center mt-4">
                {bookingsPagination.current_page > 1 && (
                  <button
                    className="px-4 py-2 bg-blue-600 text-white rounded-md mr-2"
                    onClick={() =>
                      handlePageChange(bookingsPagination.current_page - 1)
                    }
                  >
                    Previous
                  </button>
                )}
                <span className="text-gray-900">
                  {bookingsPagination.total_pages != 0 ? (
                    <>
                      Page {bookingsPagination.current_page} of{" "}
                      {bookingsPagination.total_pages}
                    </>
                  ) : (
                    <>Page 0 of 0</>
                  )}
                </span>
                {bookingsPagination.current_page <
                  bookingsPagination.total_pages && (
                  <button
                    className="px-4 py-2 bg-blue-600 text-white rounded-md ml-2"
                    onClick={() =>
                      handlePageChange(bookingsPagination.current_page + 1)
                    }
                  >
                    Next
                  </button>
                )}
              </div>
            </TabsContent>
          </Tabs>
        </main>
        <p className="absolute top-4 right-4 flex items-center justify-center h-[55px] w-[55px] bg-white rounded-full shadow-lg transition-transform hover:scale-105 hover:shadow-xl">
          <img
            className="h-[50px] w-[50px] object-cover rounded-full"
            src={Hirafic}
            alt="Logo"
          />
        </p>
      </div>
    </div>
  );
};

export default Artisan;
