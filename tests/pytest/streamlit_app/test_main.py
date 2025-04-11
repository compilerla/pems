from streamlit_app import main


def test_main(mocker):
    apps = ["app", "app"]
    mock_discover = mocker.patch("streamlit_app.main.discover_apps", return_value=apps)
    mock_navigate = mocker.patch("streamlit_app.main.st.navigation")

    main.main()

    mock_discover.assert_called_once()
    mock_navigate.assert_called_once_with(apps, position="hidden")
    mock_navigate.return_value.run.assert_called_once()
