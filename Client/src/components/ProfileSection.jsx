import React from 'react';
import { Button } from '@/components/ui/button';
import LoadingState from '@/components/LoadingState';
import ErrorState from '@/components/ErrorState';

const ProfileSection = ({ profile, loading, error, handleSubmit, handleChange, editable }) => (
  <div className="bg-gray-900 text-gray-100 p-6 rounded-lg shadow-md max-w-md mx-auto">
    {loading.profile ? <LoadingState /> : error.profile ? <ErrorState message={error.profile} /> : (
      <form onSubmit={handleSubmit} className="text-center">
        <div className="pb-4">
          <img
            src={profile?.image_file ? `http://localhost:5000/static/profile_pics/${profile.image_file}` : "http://localhost:5000/static/profile_pics/default.jpg"}
            alt="Profile"
            className="w-32 h-32 rounded-full mx-auto"
          />
        </div>
        <div className="space-y-3">
          {editable ? (
            <>
              <div className="pb-2">
                <label className="text-xs text-gray-400">Name</label>
                <input
                  type="text"
                  name="username"
                  value={profile?.username || ''}
                  onChange={handleChange}
                  className="w-full p-2 bg-gray-800 text-gray-100 rounded"
                />
              </div>
              <div className="pb-2">
                <label className="text-xs text-gray-400">Email</label>
                <input
                  type="email"
                  name="email"
                  value={profile?.email || ''}
                  onChange={handleChange}
                  className="w-full p-2 bg-gray-800 text-gray-100 rounded"
                />
              </div>
              <div className="pb-2">
                <label className="text-xs text-gray-400">Phone</label>
                <input
                  type="text"
                  name="phone_number"
                  value={profile?.phone_number || ''}
                  onChange={handleChange}
                  className="w-full p-2 bg-gray-800 text-gray-100 rounded"
                />
              </div>
              <div className="pb-2">
                <label className="text-xs text-gray-400">Location</label>
                <input
                  type="text"
                  name="location"
                  value={profile?.location || ''}
                  onChange={handleChange}
                  className="w-full p-2 bg-gray-800 text-gray-100 rounded"
                />
              </div>
              <div className="flex justify-center mt-4">
                <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                  Update Profile
                </Button>
              </div>
            </>
          ) : (
            <>
              <div className="pb-2">
                <p className="text-xs text-gray-400">Name</p>
                <p className="text-sm">{profile?.username || 'No name provided'}</p>
              </div>
              <div className="pb-2">
                <p className="text-xs text-gray-400">Email</p>
                <p className="text-sm">{profile?.email || 'No email provided'}</p>
              </div>
              <div className="pb-2">
                <p className="text-xs text-gray-400">Phone</p>
                <p className="text-sm">{profile?.phone_number || 'No phone number provided'}</p>
              </div>
              <div className="pb-2">
                <p className="text-xs text-gray-400">Location</p>
                <p className="text-sm">{profile?.location || 'No location provided'}</p>
              </div>
            </>
          )}
        </div>
      </form>
    )}
  </div>
);

export default ProfileSection;
