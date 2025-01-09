# 🎫 Streamlit + Airtable [Support Tickets Template]

A quick and easy way to manage your support tickets like a pro! This Streamlit app lets you create, manage, and visualize support tickets seamlessly using Airtable as the backend. Perfect for teams looking for a lightweight yet powerful ticketing tool. 🚀

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://airtable-support-tickets-template.streamlit.app/)
&nbsp; 
---

## ✨ Key Features

- **🔄 Full CRUD Operations**: Effortlessly create, read, update, and delete records directly in Airtable.
- **📊 Custom Sorting**: Organize and sort your data based on multiple columns for better insights.
- **📅 Smart Date Formatting**: Display dates in formats that make sense to your team.
- **📁 Multi-Table Management**: Switch and manage multiple Airtable tables without breaking a sweat.
- **🗑️ Bulk Deletion by Values/Range**: Quickly clean up your records by deleting in bulk — by specific value or range.
- **🚨 Robust Error Handling**: Never miss a beat with friendly alerts and error messages for smooth ticket management.

---

## 🛠️ Getting Started

### 1. Clone the Repo & Install Requirements

First, clone this repository and navigate to the project directory. Then, install all the necessary Python packages:

```bash
git clone <https://github.com/osamatech786/Streamlit-Airtable-Support-Tickets-Template>
cd streamlit-airtable-support-tickets
pip install -r requirements.txt
```

### 2. Configure Your Environment Variables

Rename `.env_sample` to `.env`, then add your Airtable API key, base ID, and any other required details:

```env
AIRTABLE_API_KEY=your_api_key
AIRTABLE_BASE_ID=your_base_id
```

### 3. Set Up Your Airtable Base

Create the tables in Airtable that you'll be using with the app. The structure should look something like this:

![ScreenShot](/resource/img/AirTable%20Tables.png)

> 📝 **Note**: Make sure your table structure matches the app's expected format for smooth operation.

### 4. Launch the App 🚀

You're all set! Start the app with the following command:

```bash
streamlit run app.py
```

## 🧩 Customization & Advanced Usage

- **Adjust the `.env` file**: Tweak the settings to suit your Airtable base and workflow.
- **Customize the App**: Feel free to modify the Streamlit components to match your team's needs.
- **Scalable Setup**: Need more functionality? This template can be a great starting point for building a more advanced ticketing system.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, feel free to:

1. Fork the repository.
2. Create a new branch (`feature/YourFeature`).
3. Make your changes and commit them.
4. Open a pull request describing the changes.

Let's make this app even better together!

---

## 📣 Acknowledgements

- Thanks to the [Streamlit](https://streamlit.io/) team for their amazing framework.
- Kudos to [Airtable](https://airtable.com/) for providing a user-friendly and flexible database platform.
- Inspired by community feedback and open-source contributions.
- Streamlit Community for the Template [![Streamlit Template Used](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://support-tickets-template.streamlit.app/)


---

## ⭐ Show Your Support

If this template helps you manage support tickets more effectively, please give it a ⭐ on GitHub! Your support is appreciated.

---

## 📞 Hire Me for Customization

Need help with customization, additional features, or consulting? I'm here to help! Feel free to reach out to me on [LinkedIn](https://www.linkedin.com/in/osamatech786).

---

Happy Development! 🎟️

---

<!-- ```markdown -->
## 📸 Output Screenshots

![Choose Team View](/resource/img/1_choose_team.png)
*Main dashboard showing team choose optoin*

![Create Ticket](/resource/img/2_add_a_ticket.png) 
*Create new support ticket*

![Manage Tickets](/resource/img/3_view_tickets.png)
*Ticket management interface with sorting and filtering options*

![Delete Records](/resource/img/4_delete_ticket.png)
*Bulk deletion interface for managing ticket records*

![Stats](/resource/img/5_stats.png)
*View tickets statistics*
