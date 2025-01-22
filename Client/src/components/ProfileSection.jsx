import React from 'react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import LoadingState from '@/components/LoadingState';
import ErrorState from '@/components/ErrorState';

const ProfileSection = ({ profile, loading, error, handleSubmit, handleChange, editable, handleFileChange}) => {
  const role = sessionStorage.getItem('role');

  return (
    <div className="bg-gray-900 text-gray-100 p-6 rounded-lg shadow-md max-w-md mx-auto">
      {loading.profile ? <LoadingState /> : error.profile ? <ErrorState message={error.profile} /> : (
        <form onSubmit={handleSubmit} className="space-y-4" encType="multipart/form-data">
          
          <div className="text-center">
            <img
              src={profile?.image_file ? `http://localhost:5000/static/profile_pics/${profile.image_file}` : "http://localhost:5000/static/profile_pics/default.jpeg"}
              alt="Profile"
              className="w-32 h-32 rounded-full mx-auto"
            />
            {editable && (
              <div className="mt-2 flex justify-center">
                <input
                  type="file"
                  name="image_file"
                  onChange={handleFileChange}
                  className="mt-1 block w-48 bg-gray-800 text-gray-100 rounded p-1 text-sm"
                />
              </div>
            )}
          </div>

          <div className="space-y-3">
            {editable ? (
              <>
                <FormField label="Username" type="text" name="username" value={profile?.username || ''} onChange={handleChange} />
                <FormField label="Email Address" type="email" name="email" value={profile?.email || ''} onChange={handleChange} />
                <FormField label="Phone Number" type="text" name="phone_number" value={profile?.phone_number || ''} onChange={handleChange} />
                <FormField label="Location Address" type="text" name="location" value={profile?.location || ''} onChange={handleChange} />
                {role === 'Artisan' && (
                  <>
                    <div className="pb-2">
                      <label className="text-xs text-gray-400">Profession or Specialization</label>
                      <select
                        name="specialization" 
                        value={profile?.specialization || ''}
                        onChange={handleChange}
                        className="w-full p-2 bg-gray-800 text-gray-100 rounded"
                      >
                        <option value="None">
                          Select your profession or specialization
                        </option>
                        <option value="Plumber">Plumber</option>
                        <option value="Electrician">Electrician</option>
                        <option value="Carpenter">Carpenter</option>
                        <option value="Painter">Painter</option>
                        <option value="Mechanic">Mechanic</option>
                        <option value="Technician">Technician</option>
                        <option value="Cleaner">Cleaner</option>
                        <option value="Engineering">Engineering</option>
                        <option value="Nursing">Nursing</option>
                      </select>
                    </div>
                    <FormField label="Skills" type="text" name="skills" value={profile?.skills || ''} onChange={handleChange} />
                  </>
                )}
                <div className="flex justify-center mt-4">
                  <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                    Update Profile
                  </Button>
                </div>
              </>
            ) : (
              <>
                <DisplayField label="Username" value={profile?.username || 'No name provided'} />
                <DisplayField label="Email Address" value={profile?.email || 'No email provided'} />
                <DisplayField label="Phone Number" value={profile?.phone_number || 'No phone number provided'} />
                <DisplayField label="Location Address" value={profile?.location || 'No location provided'} />
                {profile?.role === 'Artisan' && (
                  <>
                    <DisplayField label="Profession or Specialization" value={profile?.specialization || 'No profession selected'} />
                    <DisplayField label="Skills" value={profile?.skills || 'No skills provided'} />
                  </>
                )}
                <DisplayField label="Image File" value={profile?.image_file || 'No image file provided'} />
              </>
            )}
          </div>
        </form>
      )}
    </div>
  );
};

const FormField = ({ label, type, name, value, onChange }) => (
  <div className="pb-2">
    <label className="text-xs text-gray-400">{label}</label>
    <input
      type={type}
      name={name}
      value={value || ''}
      onChange={onChange}
      className="w-full p-2 bg-gray-800 text-gray-100 rounded"
    />
  </div>
);

const DisplayField = ({ label, value }) => (
  <div className="pb-2">
    <p className="text-xs text-gray-400">{label}</p>
    <p className="text-sm">{value}</p>
  </div>
);

export default ProfileSection;
